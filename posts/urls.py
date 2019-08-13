from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from .views import post_create, post_detail, post_list, post_update, post_delete

app_name = "posts"
urlpatterns = [
    url("create/", post_create),
    path("<int:id>/", post_detail, name="detail"),
    url("list/", post_list, name="list"),
    path("<int:id>/edit/", post_update, name="update"),
    path("<int:id>/delete/", post_delete),
]
