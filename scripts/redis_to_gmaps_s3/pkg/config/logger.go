package config

import (
	"os"
	"fmt"

	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
)

// strToLogLevel return a zerolog log level based on a string.
func strToLogLevel(str string) (logLevel zerolog.Level, err error) {
	levels := map[string]zerolog.Level{
		"trace":    zerolog.TraceLevel,
		"debug":    zerolog.DebugLevel,
		"info":     zerolog.InfoLevel,
		"warn":     zerolog.WarnLevel,
		"error":    zerolog.ErrorLevel,
		"fatal":    zerolog.FatalLevel,
		"panic":    zerolog.PanicLevel,
		"disabled": zerolog.Disabled,
	}

	logLevel, ok := levels[str]
	if !ok {
		err = fmt.Errorf("\"%s\" isn't a valid logging level", str)
		return
	}

	return
}

// setupLogger setup the Zerolog logger. It setup the template format that will
// be used accross the whole program like the datetime format.
func setupLogger(cfg *Config) (err error) {
	// Make logs output to the console.
	output := zerolog.ConsoleWriter{Out: os.Stdout}
	log.Logger = log.Output(output)

	// Setup lowest log level to output
	level, err := strToLogLevel(cfg.LogLevel)
	if err != nil {
		err = fmt.Errorf("failed to setup logger: %v", err)
		return
	}
	zerolog.SetGlobalLevel(level)

	log.Logger = log.With().Timestamp().Logger()
	// Customize the timestamp format if needed.
	zerolog.TimeFieldFormat = zerolog.TimeFormatUnix

	return
}
