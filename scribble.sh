/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
sudo brew update
sudo brew install python
pip install pyqt6
sudo mkdir ~/Scribble
#!/bin/bash

ZIP_URL="https://whale64.net/scribble.zip"
DOWNLOADED_ZIP="scribble.zip"
EXTRACTED_FOLDER="scribble"
DESTINATION_DIR="$HOME/Scribble"

echo "Starting the download and extraction process..."

echo "Checking for the '$DESTINATION_DIR' directory..."
if [ ! -d "$DESTINATION_DIR" ]; then
    echo "Directory not found. Creating '$DESTINATION_DIR'..."
    mkdir -p "$DESTINATION_DIR"
fi

echo "Downloading the zip file from $ZIP_URL..."
curl -s -o "$DOWNLOADED_ZIP" "$ZIP_URL"

if [ ! -f "$DOWNLOADED_ZIP" ]; then
    echo "Error: Download failed. The file '$DOWNLOADED_ZIP' was not created."
    exit 1
fi

echo "Extracting the contents of '$DOWNLOADED_ZIP'..."
unzip -q "$DOWNLOADED_ZIP" -d .

if [ ! -d "$EXTRACTED_FOLDER" ]; then
    echo "Error: Extraction failed. The folder '$EXTRACTED_FOLDER' was not found."
    rm "$DOWNLOADED_ZIP"
    exit 1
fi

echo "Moving extracted files to '$DESTINATION_DIR'..."
mv "$EXTRACTED_FOLDER"/* "$DESTINATION_DIR"

echo "Cleaning up temporary files..."
rm -r "$EXTRACTED_FOLDER"
rm "$DOWNLOADED_ZIP"

echo Done! Installed Scribble.
echo To run scribble type this:
echo 1: "cd Scribble"
echo 2: "python scribble.py"

