package pkg

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"sync"
	"time"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/service/s3"
	"github.com/google/uuid"
	"github.com/redis/go-redis/v9"
	"github.com/rs/zerolog/log"

	"provider/pkg/config"
	"provider/pkg/repositories"
)

var (
	ErrRedisQueueEmpty = errors.New("redis queue is empty")
)

// The configuration of a worker.
type WorkerConf struct {
	// The ID of the worker.
	ID string
	// The ID of the current loading.
	LoadingID string
	// The configuration for the request to the Google API.
	GoogleAPI *config.GoogleAPIConfig
	// The configuration of the connection to the Redis server.
	Redis *config.RedisConfig
	// The configuration of the S3 Bucket connection.
	S3 *config.S3Config
}

// A representation of an element retrieved from the Redis queue.
type QueueElement struct {
	// The longitude coordinate of the location.
	Longitude float64 `json:"longitude"`
	// The latitude coordinate of the location.
	Latitude float64 `json:"latitude"`
	// The road type of the location.
	RoadType string `json:"road_type"`
	// The Accident labels.
	Labels map[string]string `json:"labels"`
}

// A representation of an accident location.
type SatelitteImage struct {
	// The ID of the satellite image.
	ID string
	// The longitude coordinate of the location.
	Longitude float64
	// The latitude coordinate of the location.
	Latitude float64
	// The road type of the location (Single carriageway, Dual carriageway...)
	RoadType string
	// The labels of the sattelite image.
	Labels map[string]string
	// The downloaded image as raw bytes.
	Image []byte
}

// fetchLocation pop an element from the Redis queue of locations.
func fetchLocation(cfg *WorkerConf) (QueueElement, error) {
	ctx := context.Background()
	e := QueueElement{}
	// Pop an element from the queue
	element, err := repositories.REDIS.LPop(ctx, cfg.Redis.QueueName).Result()

	if err == redis.Nil {
		return e, ErrRedisQueueEmpty
	} else if err != nil {
		return e, err
	} else {
		// Unmarshal the json string to QueueElement structure
		if err = json.Unmarshal([]byte(element), &e); err != nil {
			return e, err
		}

		return e, nil
	}
}

// fetchSatteliteImage request to the Google Static Map API the satellite image
// for a specific location.
func fetchSatteliteImage(cfg *WorkerConf, img *SatelitteImage) error {
	reqUrl := fmt.Sprintf(
		"https://maps.googleapis.com/maps/api/staticmap?center=%f,%f&zoom=%d&size=%dx%d&format=%s&maptype=%s&key=%s",
		img.Latitude,
		img.Longitude,
		cfg.GoogleAPI.Picture.Zoom,
		cfg.GoogleAPI.Picture.Width,
		cfg.GoogleAPI.Picture.Height,
		cfg.GoogleAPI.Picture.Format,
		cfg.GoogleAPI.Picture.MapType,
		cfg.GoogleAPI.Key,
	)

	// Add the sattelite image fetching information in the labels.
	img.Labels["loaded_at"] = time.Now().Format(time.RFC3339)
	img.Labels["latitude"] = fmt.Sprintf("%f", img.Latitude)
	img.Labels["longitude"] = fmt.Sprintf("%f", img.Longitude)
	img.Labels["road_type"] = img.RoadType
	img.Labels["picture_zoom"] = fmt.Sprintf("%d", cfg.GoogleAPI.Picture.Zoom)
	img.Labels["picture_width"] = fmt.Sprintf("%d", cfg.GoogleAPI.Picture.Width)
	img.Labels["picture_height"] = fmt.Sprintf("%d", cfg.GoogleAPI.Picture.Height)

	// request sattelite image to Google API
	resp, err := http.Get(reqUrl)
	if err != nil {
		return err
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return err
	}

	img.Image = []byte(body)

	return nil
}

// pushImageToS3Bucket pushes an satellite image to a S3 bucket.
func pushImageToS3Bucket(cfg *WorkerConf, img *SatelitteImage) error {
	// Create a reader for the image data
	imgReader := bytes.NewReader(img.Image)
	metadata := make(map[string]*string)

	// Convert all labels to *string for s3.PutObject().
	for key, value := range img.Labels {
		metadata[key] = aws.String(value)
	}

	// Push satellite image to S3 Bucket.
	_, err := repositories.S3.PutObject(&s3.PutObjectInput{
		Bucket:   &cfg.S3.BucketName,
		Key:      aws.String(fmt.Sprintf("%s/%s/%s.jpg", cfg.S3.ImageFolder, img.RoadType, img.ID)),
		Body:     imgReader,
		Metadata: metadata,
	})
	if err != nil {
		return err
	}

	return nil
}

// runWorker consume a coordinate from the Redis queue to fetch the
// relative satellite images from the Google API and then push it to the defined
// S3 Bucket.
func runWorker(cfg *WorkerConf) {
	log.Info().
		Str("id", cfg.ID).
		Msg("start worker")

	for {
		// Retrieve location from Redis Queue
		element, err := fetchLocation(cfg)
		if err == ErrRedisQueueEmpty {
			log.Info().
				Str("id", cfg.ID).
				Msg("queue is empty, worker done")

			return
		} else if err != nil {
			log.Error().
				Str("id", cfg.ID).
				Err(err).
				Msg("worker failed to retrieve element from Redis queue")

			return
		}

		img := SatelitteImage{
			ID:        uuid.New().String(),
			Latitude:  element.Latitude,
			Longitude: element.Longitude,
			RoadType: element.RoadType,
			Labels:    element.Labels,
		}

		if err := fetchSatteliteImage(cfg, &img); err != nil {
			log.Error().
				Str("id", cfg.ID).
				Err(err).
				Msg("worker failed to download sattelite image from Google API")

			return
		}

		if err := pushImageToS3Bucket(cfg, &img); err != nil {
			log.Error().
				Str("id", cfg.ID).
				Err(err).
				Msg("worker failed to upload sattelite image to S3 bucket")

			return
		}

		log.Debug().
			Str("id", cfg.ID).
			Str("image_id", img.ID).
			Float64("latitude", img.Latitude).
			Float64("longitude", img.Longitude).
			Msg("successfully uploaded satellite image")
	}
}

// RunClientWorkers start all the workers to fetch and push the satellite images
// to the appropriate S3 bucket.
func RunAllWorkers(cfg *config.Config) (err error) {
	// Create wait group to ensure that program doesn't end until goroutine have
	// finished.
	var wg sync.WaitGroup

	for i := 0; uint64(i) < cfg.NbWorker; i++ {
		// Initialize the worker configuration
		workerCfg := &WorkerConf{
			ID:        uuid.New().String(), // Generate UUID as worker ID.
			LoadingID: fmt.Sprintf("%s:%s:%s", cfg.Name, cfg.Version, cfg.SessionID),
			GoogleAPI: &cfg.GoogleAPI,
			Redis:     &cfg.Redis,
			S3:        &cfg.S3,
		}
		// Add 1 goroutine to wait for
		wg.Add(1)

		// Start worker in its own goroutine
		go func(cfg *WorkerConf) {
			defer wg.Done() // Defer to signals goroutine is done as last action

			runWorker(cfg)
		}(workerCfg)
	}

	// Wait for all the go routine to finish.
	wg.Wait()

	log.Info().
		Msg("no more element in Redis queue, work done")

	return
}
