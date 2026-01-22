from ultralytics import YOLO
import os
import logging
import serial
import time


logger = logging.getLogger(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path= os.path.join(BASE_DIR,'best_openvino_model')


model = YOLO(model_path)

class DetectionBouteille:

    @staticmethod
    def detection (image_path):
        if not image_path:
            logger.error(f'aucune image pas envoyer')
            return 
        
        resultat = model.predict(image_path,conf=0.5,device='cpu',imgsz=640,verbose=False)[0]

        detection = []

        for box in resultat.boxes:

            cls = int(box.cls[0])
            conf = float(box.conf[0])
            x1,y1,x2,y2 = map(int,box.xyxy[0])

            label = model.names[conf]

            detection.append({
                "label":label,
                "conf":conf,
                "box":[x1,y1,x2,y2]
            })
