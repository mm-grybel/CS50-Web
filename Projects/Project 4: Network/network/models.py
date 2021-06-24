from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    def __str__(self):
        return f'{self.username}'


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='get_followers')

    def serialize(self, user):
        return {
            'profile_id': self.user.id,
            'username': self.user.username,
            'followers': self.followers.count(),
            'following': self.user.get_followers.count(),
            'currently_following': not user.is_anonymous and self in user.get_followers.all(),
            'can_follow': not user.is_anonymous and self.user != user
        }

    def __str__(self):
        followers = []
        all_followers = ''.join([followers.append(follower.username) for follower in self.followers.all()])
        
        return f'User #{self.user.id} - {self.user.username} - followed by {all_followers}'


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post_author')
    post = models.TextField(max_length=280)
    date_created = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(Profile, blank=True, related_name='likes')
 
    def serialize(self, user): 
        return {
            'author_id': self.author.id,
            'author_username': self.author.user.username,
            'post_id': self.id,
            'post': self.post,
            'date_created': self.date_created.strftime('%B %d, %Y, %I:%M%p'),
            'likes': self.likes.count(),
            'liked_by': not user.is_anonymous and self in Profile.objects.filter(user=user).first().likes.all(),
            'is_editable': self.author.user == user
        }

    def __str__(self):
        return f'Post #{self.id} by {self.author}: {self.post} ({self.date_created})'
