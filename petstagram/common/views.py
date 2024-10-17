from django.shortcuts import render, redirect, resolve_url
from petstagram.common.models import Like, Photo
from pyperclip import copy

def home_page(request):
    all_photos = Photo.objects.all()

    context = {
        'all_photos': all_photos
    }

    return render(request, 'common/home-page.html', context)


def like_functionality(request, photo_id: int):
    liked_object = Like.objects.filter(
        to_photo_id = photo_id,  # to_photo_id is an automatic field Django provides to reference the underlying primary key (ID) of the Photo object
    ).first()

    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_photo_id=photo_id)
        like.save()

    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')  # Redirects to fragment location on the page


def share_functionality(request, photo_id: int):
    copy(request.META.get('HTTP_HOST') + resolve_url('photo-details', photo_id))
    # HTTP_HOST = http://127.0.0.1 + photos/<int:pk> => http://127.0.0.1/photos/<int:pk>

    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')