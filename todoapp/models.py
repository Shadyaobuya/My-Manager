from ToDoApp.settings import TIME_ZONE
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields.proxy import OrderWrt


# Create your models here.



class Tasks(models.Model):
    user=models.ForeignKey(User,on_delete=CASCADE,null=True,blank=True)
    task_title=models.CharField(max_length=50,null=True)
    description=models.TextField(null=True)
    completed=models.BooleanField(default=False,null=True)
    created=models.DateTimeField(auto_now_add=True,null=True)
  

    def __str__(self):
        return self.task_title

    class Meta:
        order_with_respect_to='completed'