from django.urls import path, include
from petstagram.pets import views
from petstagram.pets.views import PetAddPage, PetDeletePage

urlpatterns = [
    path('add/', PetAddPage.as_view(), name='add-pet'),
    path('<str:username>/pet/<slug:pet_slug>/', include([
        path('', views.PetDetailsPage.as_view(), name='pet-details'),
        path('edit/', views.PetEditPage.as_view(), name='edit-pet'),
        path('delete/', PetDeletePage.as_view(), name='delete-pet'),
    ]))
]
