#!/bin/bash
# Download OECD coefficient matrix if it doesn't exist
# This runs on every Heroku dyno startup to ensure the file is always available

COEFF_FILE="/app/oecd_icio_coefficients_full.csv.gz"
DOWNLOAD_URL="https://files.manuscdn.com/user_upload_by_module/session_file/310419663031471125/xidINXGHKhgMcyvm.gz"

echo "Checking for coefficient matrix..."

if [ -f "$COEFF_FILE" ]; then
    echo "✓ Coefficient file already exists ($(du -h $COEFF_FILE | cut -f1))"
else
    echo "⚠ Coefficient file not found, downloading..."
    echo "URL: $DOWNLOAD_URL"
    
    # Download with progress
    curl -o "$COEFF_FILE" "$DOWNLOAD_URL" --progress-bar --max-time 60
    
    if [ -f "$COEFF_FILE" ]; then
        echo "✓ Download complete: $(du -h $COEFF_FILE | cut -f1)"
    else
        echo "✗ Download failed!"
        exit 1
    fi
fi

echo "Starting application..."
