from django.contrib import admin
from .models import UserProfile, Company, CompanyAccessRecord
# Register your models here.


class CompanyAccessRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'company')


admin.site.register(UserProfile)
admin.site.register(Company)
admin.site.register(CompanyAccessRecord, CompanyAccessRecordAdmin)
