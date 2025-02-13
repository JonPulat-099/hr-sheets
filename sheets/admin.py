from django.contrib import admin
from .models import (
    VacancyCategory,
    Organization,
    Vacancy,
    Candidate,
    Config,
    Country,
    Application,
)
from django.db import models
from ckeditor.fields import RichTextField


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Config._meta.fields]

    change_list_template = "admin/changelist.html"


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Application._meta.fields]


@admin.register(VacancyCategory)
class VacancyCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in VacancyCategory._meta.fields]
    formfield_overrides = {
        models.TextField: {"widget": RichTextField()},
    }


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "org_code",
        "logo",
        "email",
        "created_at",
        "sheet_url",
        "employees",
        "male_employees",
        "female_employees",
        "expatriates",
    )
    exclude = ["sheet_url"]


@admin.register(Vacancy)
class Vacancy(admin.ModelAdmin):
    list_display = [field.name for field in Vacancy._meta.fields]
    list_filter = ["created_at", "organization", "salary"]  # Example for adding filters
    search_fields = ["title", "organization__name"]

    # change_list_template = "vacancy/changelist.html"


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Candidate._meta.fields]
    # change_list_template = "candidate/changelist.html"


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Country._meta.fields]
