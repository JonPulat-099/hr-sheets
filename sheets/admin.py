from django.contrib import admin
from .models import OrganizationCategory, Organization, Vacancy, Candidate, Config


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Config._meta.fields]


@admin.register(OrganizationCategory)
class OrganizationCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "org_code",
        "category",
        "logo",
        "created_at",
        "vacancy_sheet_url",
        "candidate_sheet_url",
    )
    exclude = ("vacancy_sheet_url", "candidate_sheet_url")


@admin.register(Vacancy)
class Vacancy(admin.ModelAdmin):
    list_display = [field.name for field in Vacancy._meta.fields]
    list_filter = ["created_at", "organization", "salary"]  # Example for adding filters
    search_fields = ["title", "organization__name"]

    change_list_template = "vacancy/changelist.html"


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Candidate._meta.fields]
    change_list_template = "candidate/changelist.html"
