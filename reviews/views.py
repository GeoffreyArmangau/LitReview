from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Ticket, Review
from .forms import TicketForm, ReviewForm, FollowUserForm
from authentification.models import UserFollows, CustomUser
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value, CharField, Q
from django.urls import reverse_lazy

@login_required
def follow_users(request):
    """
    Affiche la page de gestion des abonnements et traite les actions de suivi/désabonnement.
    Attributs :
    - follow_form : formulaire pour suivre un nouvel utilisateur
    - abonnements : liste des utilisateurs que l'utilisateur actuel suit
    - abonnes : liste des utilisateurs qui suivent l'utilisateur actuel
    """
    user = request.user
    # Formulaire pour suivre un utilisateur
    if request.method == 'POST' and 'follow_user' in request.POST:
        follow_form = FollowUserForm(request.POST)
        if follow_form.is_valid():
            username = follow_form.cleaned_data['username']
            try:
                to_follow = CustomUser.objects.get(username=username)
                if to_follow == user:
                    messages.error(request, "Vous ne pouvez pas vous suivre vous-même.")
                elif UserFollows.objects.filter(user=user, followed_user=to_follow).exists():
                    messages.info(request, f"Vous suivez déjà {username}.")
                else:
                    UserFollows.objects.create(user=user, followed_user=to_follow)
                    messages.success(request, f"Vous suivez maintenant {username}.")
            except CustomUser.DoesNotExist:
                messages.error(request, "Utilisateur non trouvé.")
    else:
        follow_form = FollowUserForm()

    # Désabonnement
    if request.method == 'POST' and 'unfollow_user_id' in request.POST:
        unfollow_id = request.POST.get('unfollow_user_id')
        try:
            to_unfollow = CustomUser.objects.get(id=unfollow_id)
            UserFollows.objects.filter(user=user, followed_user=to_unfollow).delete()
            messages.success(request, f"Vous êtes désabonné de {to_unfollow.username}.")
        except CustomUser.DoesNotExist:
            messages.error(request, "Utilisateur à désabonner introuvable.")

    # Mes abonnements
    abonnements = UserFollows.objects.filter(user=user).select_related('followed_user')
    # Mes abonnés
    abonnes = UserFollows.objects.filter(followed_user=user).select_related('user')

    return render(request, 'follow_users.html', {
        'follow_form': follow_form,
        'abonnements': abonnements,
        'abonnes': abonnes,
    })

@login_required
def create_review(request):
    """
    Crée une critique avec un ticket associé.
    Attributs :
    - ticket_form : formulaire pour créer un ticket
    - review_form : formulaire pour créer une critique
    """
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('feed')
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()
    return render(request, 'create_review.html', {'ticket_form': ticket_form, 'review_form': review_form})

@login_required
def create_ticket(request):
    """
    Crée un ticket.
    Attributs :
    - form : formulaire pour créer un ticket
    """
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('feed')
    else:
        form = TicketForm()
    return render(request, 'create_ticket.html', {'form': form})

@login_required
def edit_ticket(request, ticket_id):
    """
    Modifie un ticket existant.
    Attributs :
    - form : formulaire pour modifier le ticket
    - ticket : instance du ticket à modifier
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.user != request.user:
        return HttpResponseForbidden("Vous n'avez pas le droit de modifier ce ticket.")
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'edit_ticket.html', {'form': form, 'ticket': ticket})

@login_required
@require_POST
def delete_ticket(request, ticket_id):
    """
    Supprime un ticket existant.
    Attributs :
    - ticket : instance du ticket à supprimer
    """
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    ticket.delete()
    return redirect('posts')

@login_required
def edit_review(request, review_id):
    """
    Modifie une critique existante.
    Attributs :
    - form : formulaire pour modifier la critique
    - review : instance de la critique à modifier
    """
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user:
        return HttpResponseForbidden("Vous n'avez pas le droit de modifier cette critique.")
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('posts')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'edit_review.html', {'form': form, 'review': review})

@login_required
@require_POST
def delete_review(request, review_id):
    """
    Supprime une critique existante.
    Attributs :
    - review : instance de la critique à supprimer
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('posts')

@login_required
def create_review_answer(request, ticket_id):
    """
    Permet de répondre à un ticket existant (créé par un autre utilisateur).
    Affiche le ticket et un formulaire de critique.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('feed')
    else:
        review_form = ReviewForm()
    return render(request, 'create_review_answer.html', {'ticket': ticket, 'review_form': review_form})
