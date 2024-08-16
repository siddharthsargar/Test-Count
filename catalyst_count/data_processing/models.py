from django.db import models

# Create your models here.



class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    domain = models.URLField(max_length=255, blank=True, null=True)
    year_founded = models.PositiveIntegerField(blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    size_range = models.CharField(max_length=255, blank=True, null=True)
    locality = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    linkedin_url = models.URLField(max_length=255, blank=True, null=True)
    current_employee_estimate = models.BigIntegerField(blank=True, null=True)
    total_employee_estimate = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name