from django.urls import path
from .views import (
    TicketListView,
    TicketCreateView,
    TicketDetailView,
    TicketUpdateView,
    AddCommentView,
    TicketStatusUpdateView,
    TicketDeleteView,
)

urlpatterns = [
    path("", TicketListView.as_view(), name="ticket_list"),
    path("tickets/new/", TicketCreateView.as_view(), name="ticket_create"),
    path("tickets/<int:pk>/", TicketDetailView.as_view(), name="ticket_detail"),
    path("tickets/<int:pk>/edit/", TicketUpdateView.as_view(), name="ticket_edit"),
    path("tickets/<int:pk>/comment/", AddCommentView.as_view(), name="ticket_comment"),
    path("tickets/<int:pk>/status/", TicketStatusUpdateView.as_view(), name="ticket_status_update"),
    path('tickets/<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket_delete'),
]
