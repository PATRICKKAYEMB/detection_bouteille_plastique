from django.apps import AppConfig
import os
from ultralytics import YOLO
import logging



logger = logging.getLogger(__name__)


class BouteilleAppConfig(AppConfig):
    name = "bouteille_app"

   

    yolo_model = None

    def ready(self):
        
        try:

            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(BASE_DIR,"model","best_openvino_model")
            self.yolo_model = YOLO(model_path)
            logger.info(f"modele chager avec success")
        except Exception as e:
            logger.error(f"erreur lors du chargement du  modele {e}")
            
         
