from ultralytics import YOLO

##import serial
import serial
import time
import os




arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# On pointe vers le fichier best.pt qui est dans ce MEME dossier
model_path = os.path.join(BASE_DIR, "best_openvino_model")

# On charge le modèle avec le chemin complet
try:
    model = YOLO(model_path)
    print(f"✅ Modèle chargé avec succès depuis : {model_path}")
except Exception as e:
    print(f"❌ Erreur lors du chargement du modèle : {e}")

def process_frame(image_path):
    results = model.predict(image_path, imgsz=640, conf=0.5, device="cpu", verbose=False)[0]
    

    detections = []
    detected_plastic = False

    for box in results.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        label = model.names[cls]

        detections.append({
            "label": label,
            "confidence": round(conf, 2),
            "box": [x1, y1, x2, y2]
        })

        if label == "bouteille plastique":   # adapte au nom de ta classe
            detected_plastic = True

    if detected_plastic:
        arduino.write(b'OPEN\n')

    return {
        "detected": detected_plastic,
        "detections": detections
    }




























"""



    

    import os
import time
import numpy as np
import serial
# AJOUT de l'importation indispensable
from ultralytics import YOLO 

# xConfiguration des chemins
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "best_openvino_model")
# arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
#time.sleep(2)

# Chargement du modèle
try:
    # On charge le dossier OpenVINO
    model = YOLO(model_path, task='detect')
    print(f"✅ Modèle OpenVINO chargé avec succès")
    
    # --- ASTUCE WARM-UP ---
    # On fait une détection "vide" pour réveiller le CPU
    # Cela évite le retard sur la toute première image réelle
    dummy_frame = np.zeros((320, 320, 3), dtype=np.uint8)
    model.predict(dummy_frame, imgsz=640, device="cpu", verbose=False)
    print("🔥 CPU Préchauffé et prêt pour le temps réel")
    
except Exception as e:
    print(f"❌ Erreur lors du chargement : {e}")

def process_frame(image_path):
    # Utilisation de imgsz=320 pour correspondre à l'optimisation OpenVINO
    results = model.predict(
        source=image_path, 
        imgsz=320, 
        conf=0.25, 
        device="cpu", 
        verbose=False
    )[0]

    detections = []
    detected_plastic = False

    for box in results.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        label = model.names[cls]

        

        detections.append({
            "label": label,
            "confidence": round(conf, 2),
            "box": [x1, y1, x2, y2]
        })

        if label == "bouteille plastique":   # adapte au nom de ta classe
            detected_plastic = True
    if detected_plastic:
        arduino.write(b'OPEN\n')

    return {
        "detected": detected_plastic,
        "detections": detections
    }
    """
