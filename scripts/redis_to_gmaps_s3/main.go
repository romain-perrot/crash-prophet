package main

import (
	"os"
	"fmt"
	"provider/pkg"
	"provider/pkg/config"
	"provider/pkg/repositories"
)

func main() {
	// The program config
	cfg := config.Config{}

	confPath, ok := os.LookupEnv("CONF_FILEPATH")
	if !ok {
		confPath = "./"
	}

	// Load program configuration from the redis_to_gmaps_s3.yml file.
	if err := config.Load(&cfg, confPath); err != nil {
		fmt.Print("failed to load config: {}", err)
	}

	// Initialize clients.
	repositories.InitRedisClient(&cfg.Redis)
	if err := repositories.InitS3Client(&cfg.S3); err != nil {
		fmt.Print("failed to init S3 client: {}", err)
	}
	// Ensure that Redis client will close at end of program.
	defer repositories.REDIS.Close()

	pkg.RunAllWorkers(&cfg)
}
