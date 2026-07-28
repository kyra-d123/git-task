"""Views implementing CRUD operations for sticky notes."""

from django.shortcuts import get_object_or_404, redirect, render

from .forms import NoteForm
from .models import Note


def note_list(request):
    notes = Note.objects.all().order_by("-updated_at")
    return render(request, "notes/note_list.html", {"notes": notes})


def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, "notes/note_detail.html", {"note": note})


def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save()
            return redirect("notes:note_detail", pk=note.pk)
    else:
        form = NoteForm()

    return render(request, "notes/note_form.html", {"form": form})


def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)

        if form.is_valid():
            note = form.save()
            return redirect("notes:note_detail", pk=note.pk)
    else:
        form = NoteForm(instance=note)

    return render(request, "notes/note_form.html", {"form": form})


def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)

    if request.method == "POST":
        note.delete()
        return redirect("notes:note_list")

    return render(
        request,
        "notes/note_confirm_delete.html",
        {"note": note},
    )