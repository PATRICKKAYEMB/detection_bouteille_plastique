from django.urls import path,include

from .views import detection_bouteille


urlpatterns=[
    path('detection/',detection_bouteille)
]






