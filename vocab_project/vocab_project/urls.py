from django.contrib import admin
from django.urls import path
from vocab import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('create-set/', views.create_set, name='create_set'),
    path('set/<int:set_id>/', views.study_set, name='study_set'),
    path('set/<int:set_id>/add-card/', views.add_card, name='add_card'),
    path('set/<int:set_id>/quiz/', views.quiz, name='quiz'),
    path('delete-card/<int:card_id>/', views.delete_card, name='delete_card'),
    path('delete-set/<int:set_id>/', views.delete_set, name='delete_set'),
    path('edit-card/<int:card_id>/', views.edit_card, name='edit_card'),
    path('edit-set/<int:set_id>/', views.edit_set, name='edit_set'),
]
