from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()

# Create your models here.
class Profile (models.Model):
    user: models.ForeignKey(user,on_delete=models.CASCADE)
    user_id: models.IntegerField()
    pro_image: models.ImageField(upload_to='pro_images',default='book-icon.png')
    bio: models.TextField(max_length='1000')

