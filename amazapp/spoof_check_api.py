
import requests
import base64
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


def check_image_for_spoofing(image_file):
  # file needs to be inside project/amazapp
  # with open(os.path.join(BASE_DIR, "amazapp/spoof_image.jpg"), "rb") as image_file:
  with open(image_file, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    str_1 = encoded_string.decode('utf-8')
    image_file.close()

  url = "https://ping.arya.ai/api/v1/liveness"
  payload = {"doc_base64": str_1, "req_id": "1"}
  headers = {
    'token': 'cc77f699a5363cc0a624edb348d5a14e',
    'content-type': 'application/json'
  }
  response = requests.request("POST", url, json=payload, headers=headers)
  return response
# image_file = os.path.join(BASE_DIR, "amazapp/real_image.jpg")
# print(check_image_for_spoofing(image_file).text)
