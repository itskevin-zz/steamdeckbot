import requests
from discord_webhook import DiscordWebhook
import time
from datetime import datetime
import pytz
import random

# Discord webhook URL
WEBHOOK_URL = 'https://discord.com/api/webhooks/1347085031926923327/Y8w9cZOmEXIwG7yC6Sto_5VZGpA-FRUpxgyIVGycc7pSIxQ2IgDJhSqPVRucpo15-PiO'

# Steam API Endpoint
API_URL = 'https://api.steampowered.com/IPhysicalGoodsService/CheckInventoryAvailableByPackage/v1'

# Package IDs and descriptions
PACKAGES = {
    '1202547': 'Refurbished 1TB OLED Steam Deck',
    '1202542': 'Refurbished 512GB OLED Steam Deck'
}

# Get EST Timezone
eastern = pytz.timezone('America/New_York')

def get_est_time():
    return datetime.now(eastern).strftime('%Y-%m-%d %I:%M:%S %p EST')

def check_inventory(package_id):
    params = {
        'origin': 'https://store.steampowered.com',
        'country_code': 'CA',
        'packageid': package_id
    }

    try:
        response = requests.get(API_URL, params=params)
        data = response.json()

        if 'response' in data and 'inventory_available' in data['response'] and data['response']['inventory_available']:
            message = f"✅{PACKAGES[package_id]} is available! Check Now✅! Timestamp: {get_est_time()}"
            webhook = DiscordWebhook(
                url=WEBHOOK_URL,
                content=message
            )
            webhook.execute()
            print(f"{PACKAGES[package_id]} available! Notification sent.")
        else:
            message = f"🚫{PACKAGES[package_id]} not available🚫 Timestemp: {get_est_time()}"
            webhook = DiscordWebhook(
                url = WEBHOOK_URL,
                content = message
            )
            webhook.execute()
            print(f"{PACKAGES[package_id]} not available. Checking again in 10 minutes... ({get_est_time()})")

    except Exception as e:
        print(f"Error checking {PACKAGES[package_id]}: {e}")

def main():
    print("Starting inventory checker....")
    consecutive_errors = 0  # Track API errors from Steam

    while True:  # Infinite loop
        for package_id in PACKAGES.keys():
            success = check_inventory(package_id)

            if not success: 
                consecutive_errors += 1
                if consecutive_errors >= 5: # If 5 errors, assume rate limit
                    wait_time = random.randint(420,600) 
                    print(f"Possible rate limit detected. Waiting {wait_time // 60} minutes before retrying...\n")
                    time.sleep(wait_time)
                    consecutive_errors = 0 # reset error count after waiting
            else:
                consecutive_errors = 0 # reset error count if successful
        
        wait_time = random.randint(240, 360) # waiting between 4-6 minutes
        print(f"Waiting {wait_time // 60} minutes before checking again...\n")
        time.sleep(wait_time)


if __name__ == "__main__":
    main()
