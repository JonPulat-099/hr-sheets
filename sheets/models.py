import os
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
from sheets.services.google.auth import spreadsheet_service, drive_service
from googleapiclient.errors import HttpError


class Config(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key


class OrganizationCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    vacancy_sheet_url = models.URLField(null=True, blank=True)
    candidate_sheet_url = models.URLField(null=True, blank=True)
    org_code = models.CharField(max_length=100, unique=True, null=False)
    category = models.ForeignKey(
        OrganizationCategory, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.logo:
            if os.path.isfile(self.logo.path):
                os.remove(self.logo.path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        try:
            requests = []
            requests.append({
                'addSheet': {
                    'properties': {
                        'title': f"{self.org_code}_vacancies",
                    },
                }
            })
            requests.append({
                'addSheet': {
                    'properties': {
                        'title': f"{self.org_code}_candidates"
                    },
                }
            })

            body = {"requests": requests}
            sheet = spreadsheet_service.spreadsheets().batchUpdate(
                spreadsheetId=Config.objects.get(key='sheet_id').value, body=body).execute()
            replies = sheet.get('replies')

            self.vacancy_sheet_url = f"https://docs.google.com/spreadsheets/d/{Config.objects.get(key='sheet_id').value}/edit#gid={replies[0]['addSheet']['properties']['sheetId']}"
            self.candidate_sheet_url = f"https://docs.google.com/spreadsheets/d/{Config.objects.get(key='sheet_id').value}/edit#gid={replies[1]['addSheet']['properties']['sheetId']}"
        except HttpError as err:
            print(err)

        try:
            this = Organization.objects.get(id=self.id)
            if this.logo != self.logo:
                if this.logo:
                    this.logo.delete(save=False)
        except Organization.DoesNotExist:
            pass  # when new object

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


@receiver(post_delete, sender=Organization)
def delete_image_file(sender, instance, **kwargs):
    if instance.logo and instance.logo.storage.exists(instance.logo.name):
        instance.logo.delete(save=False)


class Vacancy(models.Model):
    organization = models.ForeignKey(
        Organization, to_field="org_code", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Candidate(models.Model):
    email = models.EmailField(max_length=100)
    full_name = models.CharField(max_length=100)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=20, decimal_places=2)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
