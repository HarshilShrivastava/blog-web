from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from comments.models import comments
from django.utils import timezone
from django.utils.safestring import mark_safe
from markdown_deux import markdown


class Postmanager(models.Manager):
    def all(self):
        return super(Postmanager, self).filter(draft=False)


def upload_location(instance, Filename):
    return "%s/%s" % (instance.id, Filename)


class post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=120)
    content = models.TextField()
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=upload_location,
        height_field="width_field",
        width_field="width_field",
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    read_time = models.TimeField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    read_time = models.TimeField(null=True, blank=True)
    objects = Postmanager()

    def _unicode_(self):
        return self.title

    def _str_(self):
        return self.title

    def get_absolute_url(self):
        return "/posts/%s/" % (self.id)

    def get_markdown(self):
        content = self.content
        return mark_safe(markdown(content))

    @property
    def comments(self):
        qs = comments.objects.filter_by_instance(self)
        return qs

    @property
    def get_content_type(self):
        instance = self
        ContentTyp = ContentType.objects.get_for_model(instance.__class__)
        return ContentTyp
