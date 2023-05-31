import os
import config
os.environ["REPLICATE_API_TOKEN"] = config.replicate_api_key
import replicate
import requests
output = replicate.run(
    "jagilley/controlnet-canny:aff48af9c68d162388d230a2ab003f68d2638d88307bdaf1c2f1ac95079c9613",
    input={"image": open("./new_sketch.png", "rb"),
    		"prompt": "green velvet overalls",
    		"scale":15}
)
img_data = requests.get(output[-1]).content
with open('./controlnet_response.jpg', 'wb') as handler:
    handler.write(img_data)