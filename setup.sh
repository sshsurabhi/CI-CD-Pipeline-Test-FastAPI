#!/bin/bash
touch api_test.log
# Build the Docker images
docker-compose build

# Run the Docker Compose setup
docker-compose up
