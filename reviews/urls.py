from django.urls import path
from . import views

urlpatterns = [
	path('review/create/', views.create_review, name='create_review'),
	path('ticket/create/', views.create_ticket, name='create_ticket'),
	path('flux/', views.flux, name='flux'),
]
