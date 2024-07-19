package config

import (
	"errors"
	"strings"

	"github.com/google/uuid"
	"github.com/spf13/viper"
)

var (
	ErrConfigFileNotFound = errors.New("Config file not found")
)

type Config struct {
	// The name of the program.
	Name string
	// The version of the program.
	Version string `mapstructure:"version"`
	// The session ID of the program.
	SessionID string
	// The number of worker that will fetch and push images to the S3 Bucket.
	NbWorker uint64 `mapstructure:"nb_worker"`
	// The lowest log type that should display the server, info by default.
	LogLevel string `mapstructure:"log_level"`
	// The configuration for the request to the Google API.
	GoogleAPI GoogleAPIConfig `mapstructure:"google_api"`
	// The configuration of the connection to the Redis server.
	Redis RedisConfig `mapstructure:"redis"`
	// The configuration of the S3 Bucket connection.
	S3 S3Config `mapstructure:"s3"`
}

// A configuration for a connection to a Redis Server.
type RedisConfig struct {
	// The address of the Redis server.
	Addr string `mapstructure:"addr"`
	// The password of the Redis server.
	Password string `mapstructure:"password"`
	// The database of the Redis server to connect with.
	DB int `mapstructure:"db"`
	// The name of the queue to pop element from in the Redis server.
	QueueName string `mapstructure:"queue_name"`
}

type PictureConfig struct {
	// The zoom value of the picture.
	Zoom uint64 `mapstructure:"zoom"`
	// The width of the picture.
	Width uint64 `mapstructure:"width"`
	// The height of the picture.
	Height uint64 `mapstructure:"height"`
	// The id of the Google API map type.
	MapType string `mapstructure:"map_type"`
	// The image format (jpg, png or gif).
	Format string `mapstructure:"format"`
}

// A configuration for the request send to the Google API.
type GoogleAPIConfig struct {
	// The API key needed to enable request to the Google API.
	Key string `mapstructure:"key" validate:"required"`
	// The configuration of the picture to request to the Google API.
	Picture PictureConfig `mapstructure:"picture"`
}

// A configuration for a connection to a S3 Bucket
type S3Config struct {
	// The address of the S3 Bucket endpoint.
	Endpoint string `mapstructure:"enpoint"`
	// The region of the S3 Bucket.
	Region string
	// The name of the S3 Bucket.
	BucketName string `mapstructure:"bucket_name"`
	// The folder where satellite image will be pushed.
	ImageFolder string `mapstructure:"image_folder"`
	// The Access Key ID of the S3 Bucket.
	AccessKeyID string `mapstructure:"access_key_id" validate:"required"`
	// Access Key Secret of the S3 Bucket.
	AccessKeySecret string `mapstructure:"access_key_secret" validate:"required"`
}

// setDefaults set the default values of the program configuration
func setDefaults() {
	// Set default values
	viper.SetDefault("version", "undefined")
	viper.SetDefault("nb_worker", 1)
	viper.SetDefault("log_level", "INFO")
	viper.SetDefault("google_api.picture.zoom", "18")
	viper.SetDefault("google_api.picture.width", 400)
	viper.SetDefault("google_api.picture.height", 400)
	viper.SetDefault("google_api.picture.map_type", "satellite")
	viper.SetDefault("google_api.picture.format", "jpg")
	viper.SetDefault("redis.addr", "localhost:6379")
	viper.SetDefault("redis.db", 0)
	viper.SetDefault("redis.queue_name", "locations")
	viper.SetDefault("s3.endpoint", "s3.amazonaws.com")
	viper.SetDefault("s3.region", "pink-twins-bucket")
	viper.SetDefault("s3.image_folder", "satellite-images")
}

// Load parse both the environment and the configuration
// file if any, to fill the configuration structure of the server.
func Load(cfg *Config, path string) (err error) {
	cfg.Name = "redis_to_gmaps_s3"
	cfg.SessionID = uuid.New().String()

	// Set default values of the configuration
	setDefaults()

	// Replace env key replacer by an underscore to follow general conventions.
	viper.SetEnvKeyReplacer(strings.NewReplacer(`.`, `_`))

	// Define configuration file to viper
	viper.AddConfigPath(path)
	viper.SetConfigName("redis_to_gmaps_s3")
	viper.SetConfigType("yml")

	// Make viper read configuration file.
	err = viper.ReadInConfig()
	if err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); ok {
			err = ErrConfigFileNotFound
		}
		return
	}

	// Replace default values of configuration by variable defined in
	// environment variables of command line flags.
	viper.AutomaticEnv()

	// Fill Config structure by values from configuration fill, then environment
	// variable and finally flags (in this precise order).
	if err = viper.Unmarshal(&cfg); err != nil {
		return
	}

	return
}
