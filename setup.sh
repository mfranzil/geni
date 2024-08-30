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

sudo systemctl start postgresql

# Add PostgreSQL user
for user in /users/*; do
    user=$(basename $user)
    sudo -u postgres createuser -s $user
    sudo -u postgres createdb $user
done
