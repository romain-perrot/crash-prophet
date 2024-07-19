# Build the application from source
FROM golang:1.21 AS build-stage

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o redis_to_gmaps_s3 main.go

# Deploy the application binary into a lean image
FROM gcr.io/distroless/base-debian11 AS running-stage

WORKDIR /

ENV VERSION 0.1.0-alpha

COPY --from=build-stage /app/redis_to_gmaps_s3 /redis_to_gmaps_s3

USER nonroot:nonroot

ENTRYPOINT ["/redis_to_gmaps_s3"]
