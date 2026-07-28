"""Admin configuration for sticky notes."""

from django.contrib import admin

from .models import Note


admin.site.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """Configure notes shown in the admin interface."""

    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title", "content")
    ordering = ("-updated_at",)
