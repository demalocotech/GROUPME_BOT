import requests
import time
import uuid
from flask import Flask, request 

app = Flask(__name__)

group_id = 77687748
access_token = "LouHyWbKTMXk0z3nMSg2cEQRpWmABbhDWLfw2iLS"
Last_members = {}

@app.route("/")
def send_messages():
    message = request.args.get('message', 'Hello there!')
    response = requests.get(f"https://api.groupme.com/v3/groups/{group_id}?token={access_token}")
    if response.status_code != 200:
        return f"Error fetching group members. Error code: {response.status_code}"
    data = response.json()
    members = data["response"]["members"]
    for member in members:

      with open("user_ids.txt", "r+") as f:
        recipient_id = member["user_id"]
        content = f.read()
        if recipient_id not in content and "president" not in member["roles"]:
            f.write(recipient_id + "\n")
                
            response = requests.post(f"https://api.groupme.com/v3/direct_messages?token={access_token}", json={
                "message": {
                    "source_guid": str(uuid.uuid1()),
                    "recipient_id": recipient_id,
                    "text": message
                }
            })
            if response.status_code == 201:
                print(f"Sent message successfully to user with ID: {recipient_id}") 
            else:
                print(f"Error sending message to user with ID: {recipient_id}. Error code: {response.status_code}")
            time.sleep(3)
    return "Messages sent successfully!"


    