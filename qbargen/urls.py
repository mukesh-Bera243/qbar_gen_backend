from django.urls import path, include
from .views import *

urlpatterns = [
    path("add_qbardetails/", AddQBarDetails.as_view()),
    path('send_email/', SendEmail.as_view()),
]