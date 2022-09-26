from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.conf import settings
import uuid
from places.models import Place 


class Reels(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    place = models.ForeignKey(Place, verbose_name=_("place"), on_delete=models.CASCADE)
    en_video = models.FileField(upload_to='video', validators=[FileExtensionValidator(['mpg', 'mp2', 'mpeg', 'mpe','mpv','mp4','m4p','m4v','avchd'])])
    description = models.TextField(_("description") , null=True , blank=True)
    favourite = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Likes' , related_name='favourite')

    def __str__(self):
        return str(self.id)

    def get_likes(self):
        people = []
        likes = self.favourite.all()
        for i in likes:
            people.append(i.username)
        return {"num_likes" : len(likes) , "people": people}

    def get_likes_for_user(self , user):
        answer = False
        if user in self.favourite.all():
            answer = True
        return answer
    
    def get_comments(self):
        comment = self.comment_set.all()
        comments = []
        dic_1 = {}
        for i in comment :
            dic_1['id'] = i.id
            dic_1['username'] = i.user.username
            dic_1['comment'] = i.comment
            comments.append(dic_1)
            dic_1 = {}
        return {"num_comment" : len(comment) , "comments": comments}




class Likes(models.Model):
    reel = models.ForeignKey(Reels, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user.email)



class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reel = models.ForeignKey(Reels, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comm_date = models.DateField(("date"), auto_now_add=True)
    comment = models.CharField(max_length=500)

    def __str__(self):
        return str(self.user.email)