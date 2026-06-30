from django.db import models
from django.contrib.auth.models import User
import uuid

from django.utils import timezone
from datetime import timedelta



def default_expiry():
        return timezone.now() + timedelta(hours=24)

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="uploads/")
    original_name = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)
    download_count = models.PositiveIntegerField(default=0)
    

    share_token = models.UUIDField(
    default=uuid.uuid4,
    editable=False,
    null=True,
    blank=True
    )

    expiry_date = models.DateTimeField(default=default_expiry)


    


    def __str__(self):
        return self.original_name
