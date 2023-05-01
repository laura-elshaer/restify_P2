from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError

 
class userSerializers(ModelSerializer):
 
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'id')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token
    
class UpdateUserSerializer(ModelSerializer):
    #user = PrimaryKeyRelatedField(write_only=True, queryset = User.objects.all())
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'id')
    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise ValidationError({"username": "This username is already in use."})
        return value

    # def update(self, instance, validated_data):
    #     user = self.context['request'].user

    #     # if user.id != instance.pk:
    #     #     raise ValidationError({"authorize": "You dont have permission for this user."})

    #     instance.first_name = validated_data['first_name']
    #     instance.last_name = validated_data['last_name']
    #     instance.email = validated_data['email']
    #     instance.username = validated_data['username']
    #     instance.password = validated_data['password']

    #     instance.save()

    #     return instance
    def update(self, instance, validated_data):
        user = self.context['request'].user

        # if self.method == 'GET':
        #     old_data = {
        #         'username': instance.username,
        #         'password': instance.password,
        #         'email': instance.email,
        #         'first_name': instance.first_name,
        #         'last_name': instance.last_name,
        #     }
        #     return old_data
        # if user.id != instance.pk:
        #     raise ValidationError({"authorize": "You dont have permission for this user."})

        if self.context['request'].method == 'GET':
            return {
                'username': instance.username,
                'password': instance.password,
                'email': instance.email,
                'first_name': instance.first_name,
                'last_name': instance.last_name,
            }
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.password = validated_data['password']

        instance.save()

        return instance