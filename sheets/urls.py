from django.shortcuts import redirect
from django.urls import path
from .views import UpdateDatabase, mainStats, orgStats, getCategories, MergeSheets

urlpatterns = [
    path("", lambda request: redirect("/admin/", permanent=False)),
    path("fetch-candidate/", UpdateDatabase.as_view(), name="update_db"),
    path("merge-sheets/", MergeSheets.as_view(), name="merge_sheets"),
    path("main-stats/", mainStats, name="main_stats"),
    path("organization/<str:org_code>", orgStats, name="org_stats"),
    path("categories/<str:org_code>", getCategories, name="get_categories"),
]
