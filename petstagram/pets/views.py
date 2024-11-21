from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.gis.db.backends.postgis.const import POSTGIS_TO_GDAL
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from petstagram.common.forms import CommentForm
from petstagram.pets.forms import PetBaseForm, PetAddForm, PetEditForm, PetDeleteForm
from petstagram.pets.models import Pet


class PetAddPage(LoginRequiredMixin, CreateView):
    model = Pet
    form_class = PetAddForm
    template_name = 'pets/pet-add-page.html'
    success_url = reverse_lazy('profile-details', kwargs={'pk': 1})

    def form_valid(self, form):
        pet = form.save(commit=False)
        pet.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'profile-details',
            kwargs={'pk': self.request.user.pk}
        )


# def pet_add_page(request):
#     form = PetAddForm(request.POST or None)
#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             return redirect('profile-details', pk=1)
#     context = {
#         "form": form,
#     }
#     return render(request, 'pets/pet-add-page.html', context)

class PetEditPage(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Pet
    form_class = PetEditForm
    template_name = 'pets/pet-edit-page.html'
    slug_url_kwarg = 'pet_slug'

    def test_func(self):
        pet = get_object_or_404(Pet, slug=self.kwargs['pet_slug'])
        return self.request.user == pet.user

    def get_success_url(self):
        return reverse_lazy(
            'pet-details',
            kwargs={
                'username': self.kwargs['username'],
                'pet_slug': self.kwargs['pet_slug'],
            }
        )


# def pet_edit_page(request, username: str, pet_slug: str):
#     pet = Pet.objects.get(slug=pet_slug)
#     form = PetEditForm(request.POST or None, instance=pet)
#
#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             return redirect('pet-details', username=username, pet_slug=pet.slug)
#
#     context = {
#         'form': form,
#         'pet': pet,
#     }
#
#     return render(request, 'pets/pet-edit-page.html', context)

class PetDeletePage(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Pet
    template_name = 'pets/pet-delete-page.html'
    slug_url_kwarg = 'pet_slug'
    form_class = PetDeleteForm

    # success_url = reverse_lazy('profile-details', kwargs={'pk': 1})

    def get_success_url(self):
        return reverse_lazy(
            'profile-details',
            kwargs={
                'pk': self.request.user.pk,
            }
        )

    def test_func(self):
        pet = get_object_or_404(Pet, slug=self.kwargs['pet_slug'])
        return self.request.user == pet.user

    def get_initial(self) -> dict:
        return self.get_object().__dict__

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'data': self.get_initial(),
        })

        return kwargs


# def pet_delete_page(request, username: str, pet_slug: str):
#     pet = Pet.objects.get(slug=pet_slug)
#     form = PetDeleteForm(instance=pet)
#
#     if request.method == "POST":
#         pet.delete()
#         return redirect('profile-details', pk=1)
#
#     context = {
#         'form': form,
#         'pet': pet,
#     }
#
#     return render(request, 'pets/pet-delete-page.html', context)


class PetDetailsPage(LoginRequiredMixin, DetailView):
    model = Pet
    template_name = 'pets/pet-details-page.html'
    slug_url_kwarg = 'pet_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_photos'] = context['pet'].photo_set.all()
        context['comment_form'] = CommentForm()

        all_photos = context['pet'].photo_set.all()

        for photo in all_photos:
            photo.has_liked = photo.like_set.filter(user=self.request.user).exists()

        context['all_photos'] = all_photos

        return context

# def pet_details_page(request, username: str, pet_slug: str):
#     pet = Pet.objects.get(slug=pet_slug)
#     all_photos = pet.photo_set.all()
#     comment_form = CommentForm()
#
#     context = {
#         'pet': pet,
#         'all_photos': all_photos,
#         'comment_form': comment_form,
#     }
#
#     return render(request, 'pets/pet-details-page.html', context)
