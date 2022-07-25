from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.

class Profile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	Id_user = models.IntegerField()
	profileimg = models.ImageField(upload_to='profile_images', default='') #put the default img to be shown in the media folder, then put the name in the default path.
	location = models.CharField(max_length=100, blank=True)

