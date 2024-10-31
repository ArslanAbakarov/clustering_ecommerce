#!/bin/bash

# Check if ImageMagick is installed
if ! command -v convert &> /dev/null; then
    echo "ImageMagick is not installed. Please install it first."
    exit 1
fi

# Create an output directory if it doesn't exist
mkdir -p resized

# Loop through all images in the current directory
for img in *.{jpg,jpeg,png,gif,bmp}; do
    # Check if file exists
    if [ -f "$img" ]; then
        # Get the filename without the extension
        filename=$(basename "$img")
        # Resize the image, convert to jpg, and save with 60% quality
        convert "$img" -resize 720x720\> -quality 60 "resized/${filename%.*}.jpg"
        echo "Processed: $img"
    fi
done

echo "All images have been resized and saved to the 'resized' folder."