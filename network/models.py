from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked", blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "date": self.date.strftime("%B %d, %Y, %I:%M %p"),
            "likes": [user for user in self.likes.all().values_list('id', flat=True)]
        }


class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    person = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} has followed {self.person}"

