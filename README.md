# Refurbished Steam Deck Availability Checker

This python script can be used to check for the availability of refurbished steam deck inventory. It was written to help notify me when refurbished steam decks are available. 

## Features
- Pushes a notification to Discord when there is availability
- Randomizes the how often if calls the API to prevent rate limiting
- Automatically backs off the calls if there are multiple errors in a row
- Runs from a systemd service for auto restarts

## Installation
This was developed to be run from a raspberry pi running raspberyy pi OS. 

1. Create a systemd Service by copying the inventory-checker.service file to /etc/systemd/system/
2. Enable and Start the Service
 - `sudo systemctl enable inventory-checker`
 - `sudo systemctl start inventory-checker` 