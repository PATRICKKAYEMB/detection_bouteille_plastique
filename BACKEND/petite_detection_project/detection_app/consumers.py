import json
import asyncio
import cv2
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from .detection.detection_petite import model, RTSP_URL, process_yolo
from asgiref.sync import sync_to_async

class DetectorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.keep_running = True
        # Lancer la boucle de streaming en arrière-plan
        self.loop_task = asyncio.create_task(self.stream_rtsp())
        print("🟢 WebSocket connecté - Streaming RTSP lancé")

    async def disconnect(self, close_code):
        self.keep_running = False
        if hasattr(self, 'loop_task'):
            self.loop_task.cancel()
        print("🔴 WebSocket déconnecté")

    async def stream_rtsp(self):
        # Connexion au flux IP
        cap = cv2.VideoCapture(RTSP_URL)
        
        while self.keep_running:
            success, frame = cap.read()
            if not success:
                print("⚠️ Attente du flux RTSP...")
                await asyncio.sleep(2)
                cap = cv2.VideoCapture(RTSP_URL) # Reconnexion
                continue

            # 1. Détection (via sync_to_async car YOLO est bloquant)
            detections = await sync_to_async(process_yolo)(frame)

            # 2. Encodage de l'image pour React
            _, buffer = cv2.imencode('.jpg', frame)
            img_base64 = base64.b64encode(buffer).decode('utf-8')

            # 3. Envoi groupé
            try:
                await self.send(text_data=json.dumps({
                    "image": img_base64,
                    "detections": detections
                }))
            except Exception:
                break
            
            # Limiter à ~20 FPS pour ne pas saturer le réseau
            await asyncio.sleep(0.05)

        cap.release()