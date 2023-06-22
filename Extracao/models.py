from django.db import models

class Document(models.Model):
    uploadedFile = models.FileField(upload_to = "Upload Files/")