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

# Obtain groups
response = requests.get(
    traccar_url + "/groups",
    auth=HTTPBasicAuth(traccar_user, traccar_password),
    timeout=5,
)

groups = response.json()

# Group mapping
group_mapping = []

for group in groups:
    create_group = requests.post(
        traccar_url_target + "/groups",
        auth=HTTPBasicAuth(traccar_user_target, traccar_password_target),
        headers=headers,
        json=json.loads(json.dumps(group)),
        timeout=5,
    )

    if create_group.status_code == 200:
        group_mapping.append(
            {
                "name": group["name"],
                "id": group["id"],
                "id_target": create_group.json()["id"],
            }
        )
        print("Group created: " + group["name"])

# Save group mapping to file
with open("group_mapping.json", "w", encoding="utf-8") as outfile:
    json.dump(group_mapping, outfile)
