import os
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
from googleapiclient.errors import HttpError
from sheets.services.google.add_sheet import add_sheets_to_organization
from sheets.services.google.add_permission import permission


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
    category = models.ForeignKey(OrganizationCategory, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to="images/", blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices={"active": "Актив", "inactive": "Блокирован"},
        default="active",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True)

    def delete(self, *args, **kwargs):
        if self.logo:
            if os.path.isfile(self.logo.path):
                os.remove(self.logo.path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        try:
            spreadsheetID = Config.objects.get(key="sheet_id").value
            fileID = Config.objects.get(key="file_id").value

            if spreadsheetID and fileID:
                vacancy_url, candidate_url = add_sheets_to_organization(
                    self, spreadsheetID
                )

                self.vacancy_sheet_url = vacancy_url
                self.candidate_sheet_url = candidate_url

                #TODO: Add permission to the sheet (by email)| check and remove old permissions
                permission(self.email, spreadsheetID)
            
            else:
                print("No spreadsheetID or fileID found")

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
        Organization, to_field="org_code", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Candidate(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=20, decimal_places=2)
    country = models.CharField(max_length=100)
    state = models.CharField(
        max_length=10,
        choices={"progress": "В Процессе", "accept": "Одобрено", "reject": "Отказано"},
        default="active",
    )
    gender = models.CharField(
        choices={"male": "Мужской", "female": "Женский"}, max_length=10, default="male"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Country(models.Model):
    iso_code = models.CharField(max_length=3, unique=True)
    name_ru = models.CharField(max_length=100)
    flag = models.ImageField(upload_to="flags/", blank=True, null=True)

    def __str__(self):
        return self.name_ru
