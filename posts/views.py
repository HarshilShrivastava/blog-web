from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import post
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from comments.models import comments
from urllib import parse
from django.db.models import Q
from comments.forms import Commentform
from .forms import Postform
from .utils import get_read_time


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    fo = Postform(request.POST or None, request.FILES or None)
    if fo.is_valid():
        instance = fo.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Sucessfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {"form": fo}
    return render(request, "post_form.html", context)


def post_detail(request, id):
    instance = get_object_or_404(post, id=id)
    share_string = parse.quote(instance.title)
    intial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id,
        "content_id": instance.id,
    }
    # comment = comments.objects.filter_by_instance(instance)
    object_id = instance.id
    print(get_read_time(instance.content))
    print(get_read_time(instance.get_markdown()))

    form = Commentform(request.POST or None, initial=intial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")

        obj_id = object_id
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))

        except:
            parent_id = None
            pass
        if parent_id:
            parent_qs = comments.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = comments.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comment = instance.comments

    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "comments": comment,
        "comment_form": form,
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    queryset_list = post.objects.all().order_by("-timestamp")
    paginator = Paginator(queryset_list, 10)
    page_request_var = "page"
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    page = request.GET.get(page_request_var)
    queryset = paginator.get_page(page)
    context = {"object_list": queryset, "title": "list"}
    return render(request, "post_list.html", context)


def post_update(request, id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(post, id=id)
    fo = Postform(request.POST or None, request.FILES or None, instance=instance)
    if fo.is_valid and request.user.is_authenticated():
        instance = fo.save(commit=False)
        instance.save()
        messages.success(request, "Sucessfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {"title": instance.title, "instance": instance, "form": fo}
    return render(request, "post_form.html", context)


def post_delete(request, id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(post, id=id)
    instance.delete()
    messages.success(request, "Sucessfully created")
    return redirect("/posts/list")

