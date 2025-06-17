from django.db import models
from django.contrib.auth.models import User
import os

class LabImage(models.Model):
    category = models.CharField(max_length=100)
    file = models.FileField(upload_to='lab_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category} - {self.file.name}"

    def delete(self, *args, **kwargs):
        # Delete the file from storage
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        # Call the parent class delete method
        super().delete(*args, **kwargs)

class EveLabFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="labs")
    file = models.FileField(upload_to='eve_labs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class NetworkIssue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issues')
    lab_file = models.ForeignKey(EveLabFile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"

class ConsultancyRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultancies')
    topic = models.CharField(max_length=200)
    description = models.TextField()
    requested_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Consultancy on '{self.topic}' by {self.user.username}"