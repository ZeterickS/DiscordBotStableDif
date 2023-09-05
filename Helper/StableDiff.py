import requests
import json
import io
import base64
import datetime
from PIL import Image, PngImagePlugin

url = "http://192.168.178.21:7860"

async def Txt2ImgAPI(prompt, filename):
    payload = {
        "prompt": str(prompt),
        "steps": 25,
        "width": 900,
        "height": 700
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
        
        
async def Img2ImgAPI(input, filename, prompt):
    
    encoded = base64.b64encode(open(input, "rb").read())
    encodedString=str(encoded, encoding='utf-8')
    encodedFormated='data:image/png;base64,' + encodedString
    
    payload = {
        "prompt": prompt,
        "steps": 35,
        "width": 900,
        "height": 700,
        "init_images": [
            encodedFormated
        ]
    }
    
    response = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)
    
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