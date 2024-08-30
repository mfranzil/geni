#!/bin/bash

# Update package list
sudo apt-get update

# Install PostgreSQL
sudo apt-get install -y postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Install psql client
sudo apt-get install -y postgresql-client

echo "PostgreSQL and psql client installed and started successfully."