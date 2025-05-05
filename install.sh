#!/bin/bash

# Start the containers in detached mode
docker-compose up -d

# Wait for the containers to be healthy
echo "Waiting for containers to be healthy..."
for service in $(docker-compose ps --services); do
  # Check if the service has a healthcheck
  if docker inspect --format='{{.State.Health}}' $(docker-compose ps -q $service) &>/dev/null; then
    while [[ $(docker-compose ps -q $service | xargs docker inspect --format='{{.State.Health.Status}}') != "healthy" ]]; do
      echo "Waiting for $service to be healthy..."
      sleep 1
    done
    echo "$service is healthy."
  else
    echo "$service does not have a healthcheck. Skipping health check wait."
  fi
done

# Restart the nginx service
echo "Restarting nginx..."
docker-compose restart nginx

# Optional: Tear down the containers (comment this out if you want the app to keep running)
# echo "Stopping and removing containers..."
# docker-compose down

# Print success message
echo "App installed successfully."