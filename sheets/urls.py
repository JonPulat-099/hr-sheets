from django.urls import path
from .views import GetVacancy, GetCandidate, getMainStats

urlpatterns = [
    path("get-vacancy/", GetVacancy.as_view(), name="get_vacancy"),
    path("fetch-candidate/", GetCandidate.as_view(), name="fetch_candidate"),
    path('main-stats/', getMainStats, name='main_stats')
]
