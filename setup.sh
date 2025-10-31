#!/bin/bash

# Update package lists
sudo apt-get update

# Install system dependencies
sudo apt-get install -y ffmpeg pulseaudio alsa-utils

# Load the snd-aloop kernel module
sudo modprobe snd-aloop

echo "Server environment configured successfully."
