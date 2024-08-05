#!/bin/bash

# Function to generate a new migration
generate_migration() {
  local message=$1

  # Set database URL as an environment variable
  export ALEMBIC_DATABASE_URL=$db_url
  alembic -c ./alembic.ini revision --autogenerate -m "$message"
}

# Function to apply migrations
apply_migrations() {
  # Set database URL as an environment variable
  export ALEMBIC_DATABASE_URL=$db_url
  alembic -c ./alembic.ini upgrade head
}

# Main script
if [ "$#" -lt 1 ]; then
  echo "Usage: $0 [generate|apply] <message>"
  exit 1
fi

command=$1
db_url="postgresql://user:password@postgres/meeting_db"

if [ "$command" = "generate" ]; then
  if [ -z "$2" ]; then
    echo "Usage: $0 generate <message>"
    exit 1
  fi
  message=$2
  generate_migration "$message"
elif [ "$command" = "apply" ]; then
  apply_migrations
else
  echo "Unknown command: $command"
  exit 1
fi
