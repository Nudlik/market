from django.urls import path
from redoc_tasks.views import redoc, redoc_json

urlpatterns = [
    path('', redoc),
    path('json/', redoc_json)
]
