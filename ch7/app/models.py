from django.db import models

# Create your models here.
class Chat(models.Model):
    content = models.CharField(max_length=5000)
    timestamp = models.TimeField(auto_now_add=True)
    group = models.ForeignKey("group", on_delete=models.CASCADE)

class Group(models.Model):
    name = models.CharField(max_length=50)