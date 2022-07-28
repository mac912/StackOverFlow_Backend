"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from myapp.views import RegisterApi, CurrentUserData, CustomAuthToken, ProfileView, FollowUser, QuestionView, AnswerView, UpvoteView, RemoveUpvoteView, CommentView, AnswerUpvoteView, AnswerRemoveUpvoteView, AnswerComment

urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/register/', RegisterApi.as_view(), name="register"),
    path('api/users/currentUserData/', CurrentUserData.as_view()),
    path('api/users/login/', CustomAuthToken.as_view()),
    path('api/profiles/<str:username>/', ProfileView.as_view()),
    path('api/user/', CurrentUserData.as_view()),
    path('api/users/follow/<int:id>/', FollowUser.as_view(), name='follow'),
    path('api/questions/', QuestionView.as_view()),
    path('api/questions/<uuid:id>/', QuestionView.as_view()),
    path('api/questions/<str:id>/answers/', AnswerView.as_view()),
    path('api/questions/upvote/<str:id>/', UpvoteView().as_view()),
    path('api/questions/removeupvote/<str:id>/', RemoveUpvoteView().as_view()),
    path('api/questions/comments/<str:id>/', CommentView().as_view()),
    path('api/answers/upvote/<str:id>/', AnswerUpvoteView().as_view()),
    path('api/answers/removeupvote/<str:id>/', AnswerRemoveUpvoteView().as_view()),
    path('api/answers/comment/<str:id>/', AnswerComment.as_view()),
    #path('api/tags/', TagsView.as_view()),
]
