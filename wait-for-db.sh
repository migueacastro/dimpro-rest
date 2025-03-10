# wait-for-db.sh
#!/bin/bash
until pg_isready -h db -p 5432 -U postgres; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 2
done
exec "$@"

