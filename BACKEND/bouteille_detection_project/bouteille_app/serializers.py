from rest_framework import serializers




class DetectionUploadSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)