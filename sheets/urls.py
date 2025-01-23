from django.urls import path
from .views import GetVacancy

urlpatterns = [
    path("get-vacancy/", GetVacancy.as_view(), name="get_vacancy"),
]