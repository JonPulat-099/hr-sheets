from django.urls import path
from .views import UpdateDatabase, mainStats, orgStats, getCategories

urlpatterns = [
    path("fetch-candidate/", UpdateDatabase.as_view(), name="update_db"),

    path("main-stats/", mainStats, name="main_stats"),
    path('organization/<str:org_code>', orgStats, name='org_stats'),
    path('categories/', getCategories, name='get_categories')
]
