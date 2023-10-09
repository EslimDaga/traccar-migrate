"""Main module."""
import json
import requests


from dotenv import dotenv_values
from requests.auth import HTTPBasicAuth

config = dotenv_values(".env")

traccar_url = config["TRACCAR_URL"]
traccar_user = config["TRACCAR_USER"]
traccar_password = config["TRACCAR_PASSWORD"]

traccar_url_target = config["TRACCAR_URL_TARGET"]
traccar_user_target = config["TRACCAR_USER_TARGET"]
traccar_password_target = config["TRACCAR_PASSWORD_TARGET"]

headers = {"Content-Type": "application/json"}

# Obtain devices
response = requests.get(
    traccar_url + "/devices",
    auth=HTTPBasicAuth(traccar_user, traccar_password),
    timeout=5,
)

devices = response.json()

# Export devices to file
with open("devices.json", "w", encoding="utf-8") as outfile:
    json.dump(devices, outfile)

# Import group mapping
with open("group_mapping.json", "r", encoding="utf-8") as infile:
    group_mapping = json.load(infile)

# In device the property "groupId" replace with "id_target" from group_mapping
for device in devices:
    for group in group_mapping:
        if device["groupId"] == group["id"]:
            device["groupId"] = group["id_target"]

            # Delete propertie geofenceIds
            del device["geofenceIds"]

            # Create devices
            create_device = requests.post(
                traccar_url_target + "/devices",
                auth=HTTPBasicAuth(traccar_user_target, traccar_password_target),
                headers=headers,
                json=json.loads(json.dumps(device)),
                timeout=5,
            )

            if create_device.status_code == 200:
                print(
                    "Device created: " + device["name"] + " in group " + group["name"]
                )
            else:
                print(
                    "Error: "
                    + str(create_device.status_code)
                    + " "
                    + create_device.text
                )
