from django.shortcuts import render, get_object_or_404
from .models import comments

# Create your views here.
def comment_thread(request, abc):
    obj = get_object_or_404(comments, id=abc)
    context = {"object": obj}
    return render(request, "comment_thread.html", {})

