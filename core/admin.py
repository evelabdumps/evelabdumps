from django.contrib import admin
from .models import EveLabFile, NetworkIssue, ConsultancyRequest

admin.site.register(EveLabFile)
admin.site.register(NetworkIssue)
admin.site.register(ConsultancyRequest)