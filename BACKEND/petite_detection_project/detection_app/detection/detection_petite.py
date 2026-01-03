import os
import cv2
from ultralytics import YOLO
import os
import time
import numpy as np


# URL RTSP Hikvision (À modifier avec vos accès)
# Syntaxe: rtsp://utilisateur:motdepasse@adresse_ip:port/Streaming/Channels/101
RTSP_URL = "rtsp://admin:best2010@192.168.1.64:554/Streaming/Channels/101"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "best_openvino_model")

# Chargement du modèle
try:
    # On charge le dossier OpenVINO
    model = YOLO(model_path, task='detect')
    print(f"✅ Modèle OpenVINO chargé avec succès")
    
    # --- ASTUCE WARM-UP ---
    # On fait une détection "vide" pour réveiller le CPU
    # Cela évite le retard sur la toute première image réelle
    dummy_frame = np.zeros((320, 320, 3), dtype=np.uint8)
    model.predict(dummy_frame, imgsz=320, device="cpu", verbose=False)
    print("🔥 CPU Préchauffé et prêt pour le temps réel")
except Exception as e:
    print(f"❌ Erreur lors du chargement : {e}")
    
def process_yolo(frame):
    """Effectue la détection sur une frame et retourne les données formatées"""
    if model is None:
        return []

    # Inférence YOLO
    results = model.predict(frame, imgsz=416, conf=0.5, verbose=False)[0]
    
    detections = []
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        
        detections.append({
            "label": model.names[cls],
            "confidence": round(conf, 2),
            "box": [x1, y1, x2, y2]
        })
    return detections

    """

import os
import cv2
import serial
import time
from ultralytics import YOLO

# --- CONFIGURATION ARDUINO ---
try:
    # Remplace '/dev/ttyUSB0' par ton port réel
    arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    time.sleep(2) # Attente initialisation
    print("✅ Arduino connecté")
except Exception as e:
    arduino = None
    print(f"⚠️ Arduino non détecté : {e}")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "best.pt")
RTSP_URL = "rtsp://admin:password@192.168.1.64:554/Streaming/Channels/101"

model = YOLO(MODEL_PATH)

def process_yolo(frame):
    results = model.predict(frame, imgsz=416, conf=0.5, verbose=False)[0]
    
    detections = []
    
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        label = model.names[cls] # Récupère le nom de la classe (ex: 'plastique', 'metal')

        detections.append({
            "label": label,
            "confidence": round(conf, 2),
            "box": [x1, y1, x2, y2]
        })

        # --- LOGIQUE ARDUINO MULTI-CLASSE ---
        if arduino:
            if label == "plastique":
                arduino.write(b'P') # Envoie 'P' pour Plastique
            elif label == "metal":
                arduino.write(b'M') # Envoie 'M' pour Métal
            elif label == "verre":
                arduino.write(b'V') # Envoie 'V' pour Verre

    return detections




    
const int ledPlastique = 2; // LED Rouge
const int ledMetal = 3;     // LED Jaune
const int ledVerre = 4;     // LED Verte

void setup() {
  Serial.begin(9600);
  pinMode(ledPlastique, OUTPUT);
  pinMode(ledMetal, OUTPUT);
  pinMode(ledVerre, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char signal = Serial.read();

    // Éteindre toutes les LEDs avant d'allumer la nouvelle
    digitalWrite(ledPlastique, LOW);
    digitalWrite(ledMetal, LOW);
    digitalWrite(ledVerre, LOW);

    if (signal == 'P') {
      digitalWrite(ledPlastique, HIGH);
    } else if (signal == 'M') {
      digitalWrite(ledMetal, HIGH);
    } else if (signal == 'V') {
      digitalWrite(ledVerre, HIGH);
    }
    
    delay(500); // Garde la LED allumée un court instant
  }
}
    
 ###########################################################################################################################


def process_yolo(frame):
    results = model.predict(frame, imgsz=416, conf=0.5, verbose=False)[0]
    
    detections = []
    classes_detectees = set() # Utilise un set pour éviter les doublons

    for box in results.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        label = model.names[cls]
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        detections.append({
            "label": label,
            "confidence": round(conf, 2),
            "box": [x1, y1, x2, y2]
        })
        
        # On ajoute le label au set (ex: "plastique")
        classes_detectees.add(label)

    # --- ENVOI UNIQUE À L'ARDUINO ---
    if arduino and classes_detectees:
        # On crée une chaîne de caractères (ex: "PM" si plastique et métal sont là)
        signal = ""
        if "plastique" in classes_detectees: signal += "P"
        if "metal" in classes_detectees: signal += "M"
        if "verre" in classes_detectees: signal += "V"
        
        if signal:
            arduino.write(signal.encode()) # Envoie "PM", "PV", ou "P", etc.

    return detections


    void loop() {
  if (Serial.available() > 0) {
    // Lire toute la chaîne envoyée (ex: "PM")
    String msg = Serial.readString();

    // On éteint tout par défaut
    digitalWrite(ledPlastique, LOW);
    digitalWrite(ledMetal, LOW);
    digitalWrite(ledVerre, LOW);

    // On vérifie chaque caractère dans le message reçu
    if (msg.indexOf('P') >= 0) digitalWrite(ledPlastique, HIGH);
    if (msg.indexOf('M') >= 0) digitalWrite(ledMetal, HIGH);
    if (msg.indexOf('V') >= 0) digitalWrite(ledVerre, HIGH);
    
    // On laisse allumé 1 seconde pour que l'œil humain puisse voir
    delay(1000); 
  }
}   
    
    """