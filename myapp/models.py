from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    title=models.CharField(max_length=200)

    options=(
        ('pending','pending'),
        ('complete','complete')
    )

    status=models.CharField(max_length=200,choices=options,default='pending')

    created_date=models.DateTimeField(auto_now_add=True)

    user_object=models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title