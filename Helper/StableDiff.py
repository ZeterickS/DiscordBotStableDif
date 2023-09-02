import requests
import json
import io
import base64
import datetime
from PIL import Image, PngImagePlugin

url = "http://192.168.178.21:7860"

async def Txt2ImgAPI(prompt, requester, filename):
    payload = {
        "prompt": str(prompt),
        "negative_prompt": "nude naked",
        "steps": 25,
        "width": 800,
        "height": 600
    }

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    
    r = response.json()

    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))

        image.save(filename)
        image.save('output.png', pnginfo=pnginfo)    