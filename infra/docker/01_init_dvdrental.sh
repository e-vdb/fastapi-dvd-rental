#!/bin/bash
set -euo pipefail

# This script runs inside the official postgres container as the 'postgres' user
# It will be executed by the official entrypoint on first container start.

echo "[init] creating dvdrental database and restoring dump..."

# create database (POSTGRES_USER/POSTGRES_PASSWORD are provided via env)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
  CREATE DATABASE dvdrental;
EOSQL

# restore the archive that was mounted into /docker-entrypoint-initdb.d/
# Use --no-owner --no-privileges like in your original command
if [ -f "/docker-entrypoint-initdb.d/dvdrental.tar" ]; then
  pg_restore --no-owner --no-privileges -d dvdrental /docker-entrypoint-initdb.d/dvdrental.tar
  echo "[init] dvdrental restored successfully"
else
  echo "[init] dvdrental.tar not found; skipping restore"
fi
