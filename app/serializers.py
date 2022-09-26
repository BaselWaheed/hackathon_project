from rest_framework import serializers
from .models import Reels  , Comment
from django.utils.translation import gettext_lazy as _
import os 
from app.validation import CustomValidation
from app.secret import Data
from places.serializers import  PlaceSerializers





class VideoInfoField(serializers.FileField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_representation(self, value):
        data = super().to_representation(value)
        data = Data.encrypt(data)
        return data

    def to_internal_value(self, data):
        return data
        



class ReelsSerializers(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    place= PlaceSerializers(read_only=True)
    en_video = VideoInfoField(required=True)
    is_liked = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()

    def get_is_liked(self , obj):
        return obj.get_likes_for_user(self.context['request'].user)

    def get_likes(self,obj):
        return obj.get_likes()

    def get_comment(self,obj):
        return obj.get_comments()


    class Meta:
        model = Reels
        fields = [ 'id','user' ,'place' ,'en_video' ,'description' , 'is_liked', 'likes' , 'comment']

    def validate_en_video(self, attrs):
        list_1 = ['.mpg', '.mp2', '.mpeg', '.mpe','.mpv','.mp4','.m4p','.m4v','.avchd']
        split_tup = os.path.splitext(str(attrs))
        file_extension = split_tup[1]
        if file_extension not in list_1 :
            raise CustomValidation(_(f"you must put video type {list_1}"))
        if attrs.size > 5242880 :
            raise CustomValidation(_("the file must be less than 5 Mb "))
        return attrs

        
    def create(self, validated_data):
        reel = Reels.objects.create(**validated_data)
        return reel

    def update(self, instance, validated_data):
        try :
            reel_id =instance.data['reel_id']
            reel = Reels.objects.get(user=instance.user,id=reel_id)
        except :
            raise CustomValidation(_("you do not have permission to update or delete"))
        reel.en_video = validated_data.get('en_video', reel.en_video)
        reel.description = validated_data.get('description', reel.description)
        reel.save()
        return reel




class CommentSerializer(serializers.Serializer):
    id_reel = serializers.CharField(max_length=500 , required=True)
    comment = serializers.CharField(max_length=1000 , required=True )


    def validate_id_reel(self,attrs):
        if not Reels.objects.filter(id=attrs).exists():
            raise CustomValidation(_("the id is not match"))
        return Reels.objects.get(id=attrs)


    def save(self , user):
        comment = Comment(
            user = user ,
            reel = self.validated_data['id_reel'],
            comment = self.validated_data['comment'],
        )
        comment.save()
        return comment



class DecreptSerialziers(serializers.Serializer):
    en_video = serializers.CharField(required=True,min_length=50)

    def validate_en_video(self,attrs):
        decrypt = Data.decrpyt(attrs)
        if decrypt == False:
            raise CustomValidation(_("Data incurrpt or changed "))
        return decrypt 
