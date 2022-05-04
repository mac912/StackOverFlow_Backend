from pyexpat import model
#from api.myapp.models import Answer
from rest_framework import  serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Followers, Question, Answer, Upvote, Comment

#Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password', 'email')
        extra_kwargs = {
            'password':{'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
        password = validated_data['password'],
        email = validated_data['email'])        
        return user

#email field required but not handled  

# User serializer
class UserSerializer(serializers.ModelSerializer, TokenObtainPairSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def to_representation(self, instance):
        """Add `token` to response."""
        ret = super().to_representation(instance)
        refresh = super().get_token(instance)
        ret['token'] = str(refresh.access_token)
        return ret

    #def to_represention(self, instance):


class ProfileSerializer(serializers.ModelSerializer):
    isAdmin = serializers.BooleanField(source='is_staff', read_only=True)
    isBlocked = serializers.SerializerMethodField('is_blocked')

    class Meta:
        model = User
        fields = ('username', 'isAdmin', 'isBlocked')


    def is_blocked(self, instance):
        return not instance.is_active

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = ('__all__')

# class UpdatedUserSerializer(serializers.ModelSerializers):
#     class Meta:
#         model = User
#         fields = ('__all__')

#         def to_represention(self, instance):
#             ret = super().to_representation(instance)
#             ret[]
#             return 

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('__all__')

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('__all__')

class UpvoteSerializer(serializers.ModelSerializer):
    #questiondata = serializers.RelatedField(source='Question', read_only=True, many=True)
    class Meta:
        model = Upvote
        fields = ('__all__')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('__all__')