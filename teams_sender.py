import json
import urllib.request


def send_teams_notification(flow_url, message):
    payload = {
        "mensagem": message
    }

    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url=flow_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req) as response:
        response.read()