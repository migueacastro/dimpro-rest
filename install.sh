#!/bin/bash

# Start the containers in detached mode
docker-compose up -d

# Wait for the containers to be healthy
echo "Waiting for containers to be healthy..."
for service in $(docker-compose ps --services); do
  while [[ $(docker-compose ps -q $service | xargs docker inspect --format='{{.State.Health.Status}}') != "healthy" ]]; do
    sleep 1
  done
done

# Restart the nginx service
echo "Restarting nginx..."
docker-compose restart nginx

# Tear down the containers
echo "Stopping and removing containers..."
docker-compose down

# Print success message
echo 'App installed successfully'