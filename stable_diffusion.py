import json
import requests
import io
from PIL import Image
import config

API_URL = "https://api-inference.huggingface.co/models/SG161222/Realistic_Vision_V1.4"
api_key = config.huggingface_api_key
headers = {"Authorization": f"Bearer {api_key}"}
def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return response
clothing_description = "floor length denim overalls"
data = query("a full body, uncropped, head to toe photo of a single model wearing a "+ clothing_description + ", facing the camera, simple background")
stream = io.BytesIO(data.content)
img = Image.open(stream)
img.save("response.png")