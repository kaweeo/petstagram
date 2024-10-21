from django.shortcuts import render, redirect

from petstagram.pets.forms import PetBaseForm, PetAddForm, PetEditForm, PetDeleteForm
from petstagram.pets.models import Pet


# Create your views here.
def pet_add_page(request):
    form = PetAddForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('profile-details', pk=1)
    context = {
        "form": form,
    }
    return render(request, 'pets/pet-add-page.html', context)


def pet_edit_page(request, username: str, pet_slug: str):
    pet = Pet.objects.get(slug=pet_slug)
    form = PetEditForm(request.POST or None, instance=pet)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('pet-details', username=username, pet_slug=pet.slug)

    context = {
        'form': form,
        'pet': pet,
    }

    return render(request, 'pets/pet-edit-page.html', context)


def pet_delete_page(request, username: str, pet_slug: str):
    pet = Pet.objects.get(slug=pet_slug)
    form = PetDeleteForm(instance=pet)

    if request.method == "POST":
        pet.delete()
        return redirect('profile-details', pk=1)

    context = {
        'form': form,
        'pet': pet,
    }

    return render(request, 'pets/pet-delete-page.html', context)


def pet_details_page(request, username: str, pet_slug: str):
    pet = Pet.objects.get(slug=pet_slug)
    all_photos = pet.photo_set.all()

    context = {
        'pet': pet,
        'all_photos': all_photos,
    }

    return render(request, 'pets/pet-details-page.html', context)
