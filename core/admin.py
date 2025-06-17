from django.contrib import admin
from .models import EveLabFile, NetworkIssue, ConsultancyRequest, LabImage


@admin.register(LabImage)
class LabImageAdmin(admin.ModelAdmin):
    list_display = ('category', 'uploaded_at')
    search_fields = ('category',)

admin.site.register(EveLabFile)
admin.site.register(NetworkIssue)
admin.site.register(ConsultancyRequest)
