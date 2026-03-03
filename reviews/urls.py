from django.urls import path
from . import views

urlpatterns = [
	path('review/create/', views.create_review, name='create_review'),
	path('ticket/create/', views.create_ticket, name='create_ticket'),
	path('ticket/<int:ticket_id>/edit/', views.edit_ticket, name='edit_ticket'),
	path('ticket/<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),
	path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
	path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
	path('flux/', views.flux, name='flux'),
	path('posts/', views.posts, name='posts'),
	path('abonnements/', views.follow_users, name='follow_users'),
]
