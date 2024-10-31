#!/bin/bash

# Loop over all .webp files in the current directory
for file in *.webp; do
  # Extract the file name without the extension
  filename="${file%.webp}"
  
  # Convert .webp to .jpg
  convert "$file" "${filename}.jpg"
  
  echo "Converted $file to ${filename}.jpg"
done


for file in *.png; do
  # Extract the file name without the extension
  filename="${file%.png}"
  
  # Convert .png to .jpg
  convert "$file" "${filename}.jpg"
  
  echo "Converted $file to ${filename}.jpg"
done


for file in *.avif; do
  # Extract the file name without the extension
  filename="${file%.avif}"
  
  # Convert .avif to .jpg
  convert "$file" "${filename}.jpg"
  
  echo "Converted $file to ${filename}.jpg"
done