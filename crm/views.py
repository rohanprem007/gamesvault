from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SupportTicket

@login_required
def ticket_list(request):
    tickets = SupportTicket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'crm/ticket_list.html', {'tickets': tickets})

@login_required
def create_ticket(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        priority = request.POST.get('priority')
        message = request.POST.get('message')
        
        SupportTicket.objects.create(
            user=request.user,
            email=request.user.email,
            subject=subject,
            priority=priority,
            message=message
        )
        messages.success(request, 'Ticket created successfully!')
        return redirect('ticket_list')
        
    return render(request, 'crm/create_ticket.html')