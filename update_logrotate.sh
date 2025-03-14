#!/bin/bash

# Define paths
REPO_PATH="/home/bernd/Projects/BadGuys/bad_guys_logs"
LOGROTATE_PATH="/etc/logrotate.d/bad_guys_logs"

# Ensure the script is run as root
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

# Copy the file
cp $REPO_PATH $LOGROTATE_PATH

# Set correct permissions
chmod 644 $LOGROTATE_PATH
chown root:root $LOGROTATE_PATH

echo "Updated logrotate configuration."

