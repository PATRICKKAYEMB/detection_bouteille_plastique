import logging
import cv2
import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import DetectionUploadSerializer

# Import de ta logique métier
from .model.detection import process_frame

logger = logging.getLogger(__name__)



# --- VUE PROFESSIONNELLE ---
class DetectionBouteilleView(APIView):
    """
    API pour détecter les bouteilles plastiques et commander un Arduino.
    Supporte l'envoi de fichiers réels via multipart/form-data.
    """
    parser_classes = (MultiPartParser, FormParser)
    

    def post(self, request):
        # 1. Validation des données entrantes
        serializer = DetectionUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 2. Récupération du fichier image
        image_file = serializer.validated_data['image']

        try:
            # 3. Conversion du fichier mémoire en format compatible OpenCV
            # On lit le fichier sans l'enregistrer sur le disque (gain de performance)
            file_bytes = np.frombuffer(image_file.read(), np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            if img is None:
                return Response(
                    {"erreur": "Le fichier envoyé n'est pas une image valide."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 4. Appel de ta fonction de détection (modifiée pour accepter l'image)
            result = process_frame(img)

            # 5. Réponse Pro
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Erreur critique lors de la détection : {str(e)}")
            return Response(
                {"erreur": "Une erreur interne est survenue lors de l'analyse."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )