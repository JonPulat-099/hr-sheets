import os
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete


class OrganizationCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
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
