from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Ticket, Review
from .forms import TicketForm, ReviewForm
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST


@login_required
def create_review(request):
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
            return redirect('flux')
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()
    return render(request, 'create_review.html', {'ticket_form': ticket_form, 'review_form': review_form})

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('flux')
    else:
        form = TicketForm()
    return render(request, 'create_ticket.html', {'form': form})

@login_required
def flux(request):
    user = request.user
    month_names = [
        "janvier", "février", "mars", "avril", "mai", "juin",
        "juillet", "août", "septembre", "octobre", "novembre", "décembre"
    ]
    my_reviews = Review.objects.filter(user=user).order_by('-time_created')
    my_tickets = Ticket.objects.filter(user=user, reviews__isnull=True).order_by('-time_created')

    def format_local_date(date_value):
        local_date = timezone.localtime(date_value)
        return f"{local_date:%H:%M} {local_date.day:02d} {month_names[local_date.month - 1]} {local_date.year}"

    data = []
    for review in my_reviews:
        ticket = review.ticket
        data.append({
            'kind': 'review',
            'type': 'Vous avez posté une critique',
            'headline': review.headline,
            'rating': review.rating,
            'content': review.body,
            'date': format_local_date(review.time_created),
            'ticket_title': ticket.title if ticket else None,
            'ticket_author': ticket.user.username if ticket else None,
            'ticket_image': ticket.image.url if ticket and ticket.image else None,
        })

    for ticket in my_tickets:
        data.append({
            'kind': 'ticket',
            'type': 'Vous avez demandé une critique',
            'headline': ticket.title,
            'content': ticket.description,
            'ticket_id': ticket.id,
            'date': format_local_date(ticket.time_created),
        })

    data.sort(key=lambda item: item['date'], reverse=True)
    return render(request, "flux.html", {"flux": data})

@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.user != request.user:
        return HttpResponseForbidden("Vous n'avez pas le droit de modifier ce ticket.")
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('flux')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'edit_ticket.html', {'form': form, 'ticket': ticket})

@login_required
@require_POST
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    ticket.delete()
    return redirect('posts')

@login_required
def posts(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    # On ne veut pas afficher les tickets liés à une review créée en même temps (tickets "fantômes")
    ticket_ids_with_review = set(Review.objects.values_list('ticket_id', flat=True))
    visible_tickets = tickets.exclude(id__in=ticket_ids_with_review)
    # Prépare la liste fusionnée
    posts = list(visible_tickets)
    for review in reviews:
        posts.append(review)
    # Ajoute un attribut 'kind' pour différencier dans le template
    for post in posts:
        if isinstance(post, Ticket):
            post.kind = 'ticket'
        else:
            post.kind = 'review'
    # Trie par date décroissante
    posts.sort(key=lambda x: x.time_created, reverse=True)
    return render(request, 'posts.html', {'posts': posts})

@login_required
def edit_review(request, review_id):
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
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('posts')