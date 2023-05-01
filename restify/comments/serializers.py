from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, SerializerMethodField
from .models import Comment, ContentType
from property.models import Property
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

class CommentSerializer(ModelSerializer):
    parent_comment = PrimaryKeyRelatedField(write_only=True, queryset = Comment.objects.filter(isComment = True))
    class Meta:
        model = Comment
        exclude = ['content_type', 'object_id', 'email', 'name']
    def create(self, validated_data):
        parent_comment = validated_data.pop("parent_comment")
        return Comment.objects.create(content_object = parent_comment, isComment=False, **validated_data)

class UserCommentSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(write_only=True, queryset = User.objects.all())
    class Meta:
        model = Comment
        exclude = ['content_type', 'object_id', 'parent_comment']
    
    def create(self, validated_data):
        user = validated_data.pop("user")
        return Comment.objects.create(content_object = user, **validated_data)
    
class PropertyCommentSerializer(ModelSerializer):
    property = PrimaryKeyRelatedField(write_only=True, queryset = Property.objects.all())
    class Meta:
        model = Comment
        exclude = ['content_type', 'object_id', 'parent_comment']
    
    def create(self, validated_data):
        property = validated_data.pop("property")
        return Comment.objects.create(content_object = property, **validated_data)
    
class ReplySerializer(ModelSerializer):
    parent_comment = PrimaryKeyRelatedField(write_only=True, queryset = Comment.objects.filter(isComment = True))
    class Meta:
        model = Comment
        exclude = ['content_type', 'object_id', 'email', 'name', 'isComment']
    def create(self, validated_data):
        parent_comment = validated_data.pop("parent_comment")
        return Comment.objects.create(content_object = parent_comment, isComment=False, **validated_data)


