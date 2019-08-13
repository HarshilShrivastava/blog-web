from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from .views import comment_thread

urlpatterns = [
    path("<int:abc>/", comment_thread, name="detail"),
    # path('<int:id>/delete/' ,  comment_delete),
]

