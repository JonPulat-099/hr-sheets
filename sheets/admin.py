from django.contrib import admin
from django.shortcuts import redirect
from django.utils import timezone
from .models import OrganizationCategory, Organization, Vacancy


@admin.register(OrganizationCategory)
class OrganizationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'org_code', 'category', 'logo', 'created_at')


@admin.register(Vacancy)
class Vacancy(admin.ModelAdmin):
    list_display = [field.name for field in Vacancy._meta.fields]
    list_filter = ['created_at', 'organization',
                   'salary']  # Example for adding filters
    search_fields = ['title', 'organization__name']
    
    change_list_template = 'vacancy/changelist.html'
