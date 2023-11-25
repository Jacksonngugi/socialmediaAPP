from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

user = get_user_model()

# Create your models here.
class Profile (models.Model):
    user = models.ForeignKey(user,on_delete=models.CASCADE)
    id_user = models.IntegerField()
    pro_image = models.ImageField(upload_to='pro_images',default='book-icon.png')
    bio = models.TextField(max_length='1000',blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    user = models.CharField(max_length=100)
    user_pro = models.ForeignKey(Profile,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts')
    caption = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=datetime.now)
    no_of_like = models.IntegerField(default=0)

    def __str__(self):
        return self.user
    
class Likes(models.Model):
    username = models.CharField(max_length=100)
    post_id = models.CharField(max_length=500)

    def __str__(self):
        return self.username

class Follow(models.Model):
    follower = models.CharField(max_length=100)
    follower_pro = models.ForeignKey(Profile,on_delete=models.CASCADE)
    being_followed = models.CharField(max_length=100)

    def __str__(self):
        return self.being_followed
    
class Comment(models.Model):
    post_id = models.UUIDField()
    commenter = models.CharField(max_length=100)
    comment = models.TextField(max_length=1000)

    def __str__(self):
        return self.commenter