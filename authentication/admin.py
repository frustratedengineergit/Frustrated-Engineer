from django.contrib import admin
from .models import MemberDetail

class MemberDetailAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'email']  # Customize the displayed fields
    search_fields = ['user__username', 'phone', 'email']  # Enable searching by user's username, phone and email

admin.site.register(MemberDetail, MemberDetailAdmin)