
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver



class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.TextField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    created = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f"{self.content} by {self.user}"

    class Meta:
        ordering = ["-created"]


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.post} : {self.user}"


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')

    def __str__(self):
        return self.user.username
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


