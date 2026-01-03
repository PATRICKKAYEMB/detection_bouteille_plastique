import json
import base64
import cv2
import numpy as np
from channels.generic.websocket import AsyncWebsocketConsumer
 
from .model.detection import process_frame
from asgiref.sync import sync_to_async

class DetectorConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        print("🟢 WebSocket connected")

    async def disconnect(self, close_code):
        print("🔴 WebSocket disconnected")

    async def receive(self, text_data):
        # 1️⃣ Convert JSON texte → dictionnaire
        data = json.loads(text_data)

        # 2️⃣ Récupérer la frame encodée en base64
        image_base64 = data.get("image")
        if not image_base64:
            return

        # 3️⃣ Décoder base64 → OpenCV image
        img_bytes = base64.b64decode(image_base64)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # 4️⃣ Appel de YOLO (async pour ne pas bloquer)
        result = await sync_to_async(process_frame)(frame)

        # 5️⃣ Envoyer le résultat à React
        await self.send(text_data=json.dumps(result))
