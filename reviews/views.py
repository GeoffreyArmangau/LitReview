
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Ticket, Review
from .forms import TicketForm, ReviewForm


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
    return render(request, 'reviews/create_review.html', {'ticket_form': ticket_form, 'review_form': review_form})

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
    return render(request, 'reviews/create_ticket.html', {'form': form})
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