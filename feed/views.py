from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.db.models import Q, CharField, Value
from itertools import chain
from reviews.models import Ticket, Review
from authentification.models import UserFollows
from django.shortcuts import redirect

def feed(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    def get_users_viewable_tickets(user):
        # Tickets de l'utilisateur et des utilisateurs suivis
        followed_users = UserFollows.objects.filter(
            user=user).values_list(
                'followed_user', flat=True
                )
        tickets = Ticket.objects.filter(
            Q(user=user) | Q(user__in=followed_users)
        )
        return tickets.annotate(
            content_type=Value('TICKET', CharField())
            )

    def get_users_viewable_reviews(user):
        # Reviews de l'utilisateur, des suivis, et reviews sur les tickets de l'utilisateur
        followed_users = UserFollows.objects.filter(
            user=user).values_list(
                'followed_user', flat=True
                )
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
    return render(
        request,
        'feed/feed.html',
        {
            'posts': posts
        }
    )


class PostListView(LoginRequiredMixin, ListView):
    """
    Vue pour afficher les posts de l'utilisateur connecté.
    """
    template_name = 'feed/post.html'
    context_object_name = 'posts'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        user = self.request.user
        tickets = Ticket.objects.filter(user=user).order_by('-time_created')
        user_reviews = Review.objects.filter(user=user).order_by('-time_created')
        reviews_on_user_tickets = Review.objects.filter(ticket__user=user).exclude(user=user)
        reviews_by_ticket = {}
        for review in reviews_on_user_tickets:
            reviews_by_ticket.setdefault(review.ticket_id, []).append(review)

        posts = []
        for review in user_reviews:
            review.kind = 'review'
            posts.append(review)
        for ticket in tickets:
            ticket.kind = 'ticket'
            posts.append(ticket)
            for review in reviews_by_ticket.get(ticket.id, []):
                review.kind = 'review'
                posts.append(review)
        return posts
