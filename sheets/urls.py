from django.urls import path
from .views import GetVacancy, GetCandidate, mainStats, orgStats, getCategories

urlpatterns = [
    path("get-vacancy/", GetVacancy.as_view(), name="get_vacancy"),
    path("fetch-candidate/", GetCandidate.as_view(), name="fetch_candidate"),

    path("main-stats/", mainStats, name="main_stats"),
    path('organization/<str:org_code>', orgStats, name='org_stats'),
    path('categories/', getCategories, name='get_categories')
]
