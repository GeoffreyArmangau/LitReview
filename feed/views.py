
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.db.models import Q, CharField, Value
from itertools import chain
from reviews.models import Ticket, Review
from authentification.models import UserFollows

def feed(request):
    user = request.user

    def get_users_viewable_tickets(user):
        # Tickets de l'utilisateur et des utilisateurs suivis
        followed_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)
        tickets = Ticket.objects.filter(Q(user=user) | Q(user__in=followed_users))
        return tickets.annotate(content_type=Value('TICKET', CharField()))

    def get_users_viewable_reviews(user):
        # Reviews de l'utilisateur, des suivis, et reviews sur les tickets de l'utilisateur
        followed_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)
        reviews = Review.objects.filter(
            Q(user=user) |
            Q(user__in=followed_users) |
            Q(ticket__user=user)
        )
        return reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_users_viewable_tickets(user)
    reviews = get_users_viewable_reviews(user)
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'feed/feed.html', {'posts': posts})

class PostListView(LoginRequiredMixin, ListView):
    """
    Vue pour afficher les posts (tickets et critiques) de l'utilisateur connecté.
    """
    template_name = 'feed/post.html'
    context_object_name = 'posts'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        user = self.request.user
        tickets = Ticket.objects.filter(user=user).order_by('-time_created')
        reviews = Review.objects.filter(Q(user=user) | Q(ticket__user=user))
        reviews_by_ticket = {}
        for review in reviews:
            reviews_by_ticket.setdefault(review.ticket_id, []).append(review)
        # On prépare une liste où chaque ticket est suivi de sa/son review(s) associée(s)
        posts = []
        for ticket in tickets:
            ticket.kind = 'ticket'
            posts.append(ticket)
            for review in reviews_by_ticket.get(ticket.id, []):
                review.kind = 'review'
                posts.append(review)
        return posts
