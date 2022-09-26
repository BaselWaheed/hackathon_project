from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid



class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cat_name = models.CharField(_("name"), max_length=70)

    def __str__(self):
        return self.cat_name
    


class Place(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    place_name = models.CharField(_("name"), max_length=70)
    governorate = models.CharField(_("governorate"), max_length=70)
    category = models.ForeignKey(Category, verbose_name=_("category"), on_delete=models.CASCADE)

    def __str__(self):
        return self.place_name