#!/bin/bash
set -e

echo "🏁 Starting dvdrental initialization..."

# Wait until Postgres is ready
until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "⏳ Waiting for Postgres to be ready..."
  sleep 2
done

# Restore dvdrental only if the database is empty
if ! psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT 1 FROM rental LIMIT 1;" > /dev/null 2>&1; then
  echo "⏳ Restoring dvdrental.tar into database '$POSTGRES_DB'..."
  pg_restore --no-owner --no-privileges -d "$POSTGRES_DB" /docker-entrypoint-initdb.d/dvdrental.tar
  echo "✅ dvdrental data imported successfully."
else
  echo "✅ dvdrental already initialized — skipping restore."
fi
