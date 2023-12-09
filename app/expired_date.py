from datetime import datetime, timezone
from fastapi import HTTPException
import pytz
import json

def convert_iso_to_dhaka_time():
    try:
        with open("app/credentials/access-refresh-token.json", 'r') as json_file:
            data = json.load(json_file)
        
        iso_string = data["token_expiry"]
        # Parse the ISO string to a datetime object
        utc_time = datetime.fromisoformat(iso_string.replace('Z', '+00:00')).replace(tzinfo=timezone.utc)

        # Define the Asia/Dhaka timezone
        dhaka_timezone = pytz.timezone('Asia/Dhaka')

        # Convert the time to Asia/Dhaka timezone
        dhaka_time = utc_time.astimezone(dhaka_timezone)

        # Format the time in AM/PM format
        formatted_time = dhaka_time.strftime("%Y-%m-%d %I:%M:%S %p")

        return "Asia/Dhaka Time (AM/PM):" + formatted_time
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))