from django.db import models
from django.contrib.auth.models import User
import uuid


class Followers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='followers_followers')

    # def __str__(self):
    #     return self.user.id

class Question(models.Model):
    tags = models.TextField(null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, default='Hello')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_by_auther')

class Answer(models.Model):
    ansId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_by_auther')
    questionId = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    answer = models.ForeignKey(Answer, null=True, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    comment = models.TextField()

class Upvote(models.Model):
    answer = models.ForeignKey(Answer, null=True, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    upvoteBy = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    upvoteCount = models.IntegerField(default=0)

