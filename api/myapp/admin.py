from django.contrib import admin
from .models import Followers, Question, Answer, Comment, Upvote

# Register your models here.
admin.site.register(Followers)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(Upvote)

