import cv2
import os
import numpy as np
from ultralytics import YOLO

# --- Configuration des chemins ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "mon_detection_bouteille")  # dossier OpenVINO exporté

# --- Chargement du modèle ---
try:
    model = YOLO(model_path, task='detect')
    print("✅ Modèle OpenVINO chargé avec succès")

    # --- Warm-up CPU pour éviter le lag sur la première image ---
    dummy_frame = np.zeros((320, 320, 3), dtype=np.uint8)
    model.predict(dummy_frame, imgsz=320, device="cpu", verbose=False)
    print("🔥 CPU prêt pour la détection temps réel")
except Exception as e:
    print(f"❌ Erreur lors du chargement : {e}")
    exit(1)

# --- Ouvrir la caméra ---
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Impossible d'ouvrir la caméra")
    exit(1)

print("📷 Appuyez sur 'q' pour quitter")

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Image non capturée")
        break

    # --- Détection ---
    results = model.predict(frame, imgsz=320, conf=0.25, device="cpu", verbose=False)[0]

    for box in results.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        label = model.names[cls]
        text = f"{label}: {conf:.2f}"

        # Dessiner la boîte et le label
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # --- Affichage temps réel ---
    cv2.imshow("Détection OpenVINO YOLO", frame)

    # Quitter avec 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

