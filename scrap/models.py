from django.db import models

# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=60,unique=True)
    info=models.CharField(max_length=300)
    status=models.BooleanField(default=False)
    
