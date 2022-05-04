from multiprocessing.connection import answer_challenge
from unicodedata import name
from urllib import response
from .models import Question
from rest_framework import generics
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer, ProfileSerializer, QuestionSerializer, AnswerSerializer, UpvoteSerializer, CommentSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Followers, Answer, Upvote, Comment



#Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
        })

class CurrentUserData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = RegisterSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(ObtainAuthToken):

    Permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'email': user.email
        })


class ProfileView(APIView):
    authentication_classes = ()
    Permission_classes = ()

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

class  FollowUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        user_to_follow = User.objects.get(id=id)
        session_user = request.user
        try:    
            add_usr = Followers.objects.get(user=session_user)
            print(add_usr, add_usr.followers.all())
            # add_usr.followers.add(user_to_follow)
        except Followers.DoesNotExist as err:
            print(str(err))
            add_usr = Followers.objects.create(user=session_user)
        add_usr.followers.add(user_to_follow)

        return Response({})

class QuestionView(APIView):
    Permission_classes = (IsAuthenticated)

    def get(self, request):
        #serializer = QuestionSerializer()
        dat = Question.objects.all()
        serializer = QuestionSerializer(dat, many=True)
        print(dat)
        return Response(serializer.data) 

    def post(self, request, *args, **kwargs):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            print(question)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        question = Question.objects.get(id=id)
        print(question)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnswerView(APIView):
    Permission_classes = (IsAuthenticated)
    def post(self, request, id, *args, **kwargs):
        data = request.data
        data['questionId'] = id
        serializer = AnswerSerializer(data=data)
        if serializer.is_valid():
            answer = serializer.save()
            print('answer', answer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        dat = Answer.objects.all()
        serializer = AnswerSerializer(dat, many=True)
        return Response(serializer.data)

class UpvoteView(APIView):
    Permission_classes = (IsAuthenticated)
    def get(self, request, id):
        #print(a)
        a = Question.objects.get(id=id)
        dat = Upvote.objects.filter(question=a).first()
        if(dat):
            dat.upvoteCount = dat.upvoteCount + 1
            dat.save()
        else:
            dat = Upvote.objects.create(upvoteCount=1, question=a)
        dat = Upvote.objects.all()
        serializer = UpvoteSerializer(dat, many=True)
        return Response(serializer.data)

class RemoveUpvoteView(APIView):
    Permission_classes = (IsAuthenticated)
    def get(self, request, id):
        a = Question.objects.get(id=id)
        dat = Upvote.objects.filter(question=a).first()
        if(dat):
            dat.upvoteCount = dat.upvoteCount - 1
            dat.save()
        else:
            dat = Upvote.objects.create(upvoteCount=1, question=a)
        dat = Upvote.objects.all()
        serializer = UpvoteSerializer(dat, many=True)
        return Response(serializer.data)

class CommentView(APIView):
    Permission_classes = (IsAuthenticated)
    def post(self, request, id, *args, **kwargs):
        data = request.data
        data['question'] = id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            answer = serializer.save()
           # print('answer', answer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnswerUpvoteView(APIView):
    Permission_classes = (IsAuthenticated)
    def get(self, request, id):
        a = Answer.objects.get(ansId=id)
        dat = Upvote.objects.filter(answer=a).first()
        if(dat):
            dat.upvoteCount = dat.upvoteCount + 1
            dat.save()
        else:
            dat = Upvote.objects.create(upvoteCount=1, answer=a)
        dat = Upvote.objects.all()
        serializer = UpvoteSerializer(dat, many=True)
        return Response(serializer.data)

class AnswerRemoveUpvoteView(APIView):
    Permission_classes = (IsAuthenticated)
    def get(self, request, id):
        a = Answer.objects.get(ansId=id)
        dat = Upvote.objects.filter(answer=a).first()
        if(dat):
            dat.upvoteCount = dat.upvoteCount - 1
            dat.save()
        else:
            dat = Upvote.objects.create(upvoteCount=1, answer=a)
        dat = Upvote.objects.all()
        serializer = UpvoteSerializer(dat, many=True)
        return Response(serializer.data)

class AnswerComment(APIView):
    Permission_classes = (IsAuthenticated)
    def post(self, request, id, *args, **kwargs):
        data = request.data
        data['answer'] = id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            answer = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class TagsView(APIView):
#     Permission_classes = (IsAuthenticated)
#     def get(self, request):
#         obj = Question.objects.all()
#         for i in range(0, 2):
#             list = obj[i].tags
#         print(list)
#         return Response({})

















