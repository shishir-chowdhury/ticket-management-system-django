from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import TicketForm, CommentForm
from .models import Ticket, Attachment, Comment

class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    context_object_name = "tickets"
    template_name = "tickets/ticket_list.html"
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        status = self.request.GET.get("status", "")
        base = Ticket.objects.select_related("created_by", "assigned_to").order_by("-created_at")
        if not self.request.user.is_staff:
            base = base.filter(Q(created_by=self.request.user) | Q(assigned_to=self.request.user))
        if q:
            base = base.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if status:
            if status not in dict(Ticket.STATUS_CHOICES).keys():
                messages.error(self.request, "Invalid status filter.")
                return base.none()
            base = base.filter(status=status)
        return base

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = "tickets/ticket_form.html"
    success_url = reverse_lazy("ticket_list")

    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.created_by = self.request.user
        ticket.save()
        for f in self.request.FILES.getlist("attachments"):
            Attachment.objects.create(ticket=ticket, file=f)
        messages.success(self.request, "Ticket created successfully.")
        return redirect("ticket_detail", pk=ticket.pk)

class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    context_object_name = "ticket"
    template_name = "tickets/ticket_detail.html"

    def get_queryset(self):
        qs = super().get_queryset().select_related("created_by", "assigned_to").prefetch_related("comments", "attachments")
        if self.request.user.is_staff:
            return qs
        return qs.filter(Q(created_by=self.request.user) | Q(assigned_to=self.request.user))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comment_form"] = CommentForm()
        return ctx

class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = "tickets/ticket_form.html"

    def get_queryset(self):
        qs = Ticket.objects.all()
        if self.request.user.is_staff:
            return qs
        return qs.filter(Q(created_by=self.request.user) | Q(assigned_to=self.request.user))

    def form_valid(self, form):
        ticket = form.save()
        for f in self.request.FILES.getlist("attachments"):
            Attachment.objects.create(ticket=ticket, file=f)
        messages.success(self.request, "Ticket updated.")
        return redirect("ticket_detail", pk=ticket.pk)

class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)

        if not (request.user.is_staff or ticket.created_by == request.user or ticket.assigned_to == request.user):
            messages.error(request, "You don't have permission to comment on this ticket.")
            return redirect("ticket_list")

        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(ticket=ticket, author=request.user, body=form.cleaned_data["body"])
            messages.success(request, "Comment added.")
        else:
            messages.error(request, "Please write a valid comment.")
        return redirect("ticket_detail", pk=pk)


class TicketStatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        ticket = get_object_or_404(Ticket, pk=pk)

        # Permission check
        if not (request.user.is_staff or ticket.created_by == request.user or ticket.assigned_to == request.user):
            messages.error(request, "You don't have permission to update this ticket.")
            return redirect("ticket_list")

        # Get status from POST data
        status = request.POST.get("status")
        if status not in dict(Ticket.STATUS_CHOICES).keys():
            messages.error(request, "Invalid status.")
        else:
            ticket.status = status
            ticket.save()
            messages.success(request, f"Ticket status changed to {ticket.get_status_display()}.")

        return redirect("ticket_detail", pk=ticket.pk)
