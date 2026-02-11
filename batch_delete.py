import requests
import os
from dotenv import load_dotenv


image_ids = []

run = False
while not run:
    image_id = str(input("Piwigo ID to delete (type run to run, exit to exit): ")).strip()
    if image_id == 'run':
        run = True
        break

    if image_id == 'exit':
        quit()

    image_ids.append(image_id)

print("Images to delete:")
for image_id in image_ids:
    print({image_id}, end=', ')

print(end='\n')

if image_ids:
    load_dotenv()
    API_KEY = os.getenv("API_KEY")

    HEADERS = {"X-PIWIGO-API": API_KEY}
    PIWIGO_URL = "https://mines.piwigo.com/ws.php?format=json"

    session = requests.Session()
    session.headers.update(HEADERS)

    # 1. get pwg_token
    r = session.post(PIWIGO_URL, data={"method": "pwg.session.getStatus"}, timeout=30)
    js = r.json()

    if js.get("stat") != "ok":
        raise RuntimeError(js)

    pwg_token = js["result"]["pwg_token"]

    payload = {
        "method": "pwg.images.delete",
        "image_id": ";".join(map(str, image_ids)),
        "pwg_token": pwg_token,
    }

    r = session.post(PIWIGO_URL, data=payload, timeout=30)
    print(r.json())
