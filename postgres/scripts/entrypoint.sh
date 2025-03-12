#!/bin/bash

# Load backup on start
if [ -f /backups/backup.sql ]; then
  echo "Loading backup..."
  psql -U postgres -d postgres -f /backups/backup.sql
fi

# Execute the original entrypoint
exec /usr/local/bin/docker-entrypoint.sh "$@"

# Dump the database on stop
function cleanup {
  echo "Dumping database..."
  pg_dump -U postgres -d postgres -f /backups/backup.sql
}
trap cleanup EXIT
