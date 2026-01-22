
from ultralytics import YOLO
import os



##arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
##time.sleep(2)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# On pointe vers le fichier best.pt qui est dans ce MEME dossier
model_path = os.path.join(BASE_DIR, "best.pt")

# On charge le modèle avec le chemin complet
try:
    model = YOLO(model_path)
    print(f"✅ Modèle chargé avec succès depuis : {model_path}")
except Exception as e:
    print(f"❌ Erreur lors du chargement du modèle : {e}")
    
model.export(format="openvino", imgsz=480)
