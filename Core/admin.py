from django.contrib import admin
from .models import UserProfile, Company, CompanyAccessRecord
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Company)
admin.site.register(CompanyAccessRecord)