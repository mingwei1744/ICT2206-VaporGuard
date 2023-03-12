#!/bin/bash
# Script4. Moving PHP codes to html directory

# source directory
source_dir="/tmp/*.php"

# destination directory
destination_dir="/var/www/html"

# move all files from source directory to destination directory
mv $source_dir $destination_dir