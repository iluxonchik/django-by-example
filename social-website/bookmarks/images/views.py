import redis
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ImageCreateForm
from django.contrib.auth.decorators import login_required
from .models import Image
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action

# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

@login_required
def image_create(request):
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            # assign current user tot the item
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'bookmarked image', new_item)
            messages.success(request, 'Image added sucessfully')

            # redirect user to new created item detail view
            return redirect(new_item.get_absolute_url())
    else:
        # build the form with data provided bu the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)
    return render(request, 'images/image/create.html', {'section':'images', 'form':form})

def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # increment total image views
    total_views = r.incr('image:{}:views'.format(image.id))
    # increment image ranking by 1
    r.zincrby('image_ranking', image.id, 1)
    return render(request, 'images/image/detail.html', {'section':'images', 'image':image, 'total_views':total_views})

@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})

def image_list(request):
    """
    View that takes care of displaying the image list. The same view is used to handle
    AJAX and non-AJAX requests, each one using a different template.
    """
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
         images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # The the request is AJAX and the page is out of range, return an empty page,
            # this will prevent the AJAX request from appending more content to the page
            return HttpResponse('')
        # If page is out of range, but the request is not AJAX, deliver the last page
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 
            'images/image/list_ajax.html',  # tempalte that handles AJAX requests for image list
            {
                'section': 'images',
                'images': images,
            })
    return render(request,
        'images/image/list.html',  # tempalte that handles non-AJAX reqeuests for image list
        {
            'section': 'images', 
            'images': images,
        })

@login_required
def image_ranking(request):
    # get image ranking dictionary
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # get most viewed images
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))  # force QuerySet evaluation, since we use sort() below
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request, 'images/image/ranking.html', {'section':'images', 'most_viewed':most_viewed})
