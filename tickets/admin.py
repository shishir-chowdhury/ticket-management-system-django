from django.contrib import admin
from .models import Ticket, Comment, Attachment

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ("created_at",)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "priority", "created_by", "assigned_to", "created_at")
    list_filter = ("status", "priority", "assigned_to")
    search_fields = ("title", "description")
    inlines = [AttachmentInline, CommentInline]

admin.site.register(Comment)
admin.site.register(Attachment)
