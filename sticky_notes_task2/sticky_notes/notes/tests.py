from django.test import TestCase
from django.urls import reverse

from .forms import NoteForm
from .models import Note


class NoteModelTest(TestCase):
    """Tests for the Note model."""

    def setUp(self):
        self.note = Note.objects.create(
            title="Test Note",
            content="This is a test note.",
        )

    def test_note_has_correct_title(self):
        self.assertEqual(self.note.title, "Test Note")

    def test_note_has_correct_content(self):
        self.assertEqual(
            self.note.content,
            "This is a test note.",
        )

    def test_note_string_representation(self):
        self.assertEqual(str(self.note), "Test Note")


class NoteFormTest(TestCase):
    """Tests for the Note form."""

    def test_form_is_valid_with_correct_data(self):
        form = NoteForm(
            data={
                "title": "New Note",
                "content": "This is a new note.",
            }
        )

        self.assertTrue(form.is_valid())

    def test_form_is_invalid_without_title(self):
        form = NoteForm(
            data={
                "title": "",
                "content": "A note without a title.",
            }
        )

        self.assertFalse(form.is_valid())

    def test_form_is_invalid_without_content(self):
        form = NoteForm(
            data={
                "title": "Incomplete Note",
                "content": "",
            }
        )

        self.assertFalse(form.is_valid())


class NoteViewTest(TestCase):
    """Tests for the Sticky Notes views."""

    def setUp(self):
        self.note = Note.objects.create(
            title="Test Note",
            content="This is a test note.",
        )

    def test_note_list_view(self):
        response = self.client.get(
            reverse("notes:note_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")
        self.assertTemplateUsed(
            response,
            "notes/note_list.html",
        )

    def test_note_detail_view(self):
        response = self.client.get(
            reverse(
                "notes:note_detail",
                args=[self.note.pk],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")
        self.assertContains(
            response,
            "This is a test note.",
        )
        self.assertTemplateUsed(
            response,
            "notes/note_detail.html",
        )

    def test_note_create_view_get_request(self):
        response = self.client.get(
            reverse("notes:note_create")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "notes/note_form.html",
        )

    def test_note_create_view_post_request(self):
        response = self.client.post(
            reverse("notes:note_create"),
            {
                "title": "Created Note",
                "content": "Created during a test.",
            },
        )

        self.assertEqual(Note.objects.count(), 2)

        created_note = Note.objects.get(
            title="Created Note"
        )

        self.assertEqual(
            created_note.content,
            "Created during a test.",
        )

        self.assertRedirects(
            response,
            reverse(
                "notes:note_detail",
                args=[created_note.pk],
            ),
        )

    def test_note_update_view(self):
        response = self.client.post(
            reverse(
                "notes:note_update",
                args=[self.note.pk],
            ),
            {
                "title": "Updated Note",
                "content": "The note was updated.",
            },
        )

        self.note.refresh_from_db()

        self.assertEqual(
            self.note.title,
            "Updated Note",
        )

        self.assertEqual(
            self.note.content,
            "The note was updated.",
        )

        self.assertRedirects(
            response,
            reverse(
                "notes:note_detail",
                args=[self.note.pk],
            ),
        )

    def test_note_delete_confirmation_page(self):
        response = self.client.get(
            reverse(
                "notes:note_delete",
                args=[self.note.pk],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")
        self.assertTemplateUsed(
            response,
            "notes/note_confirm_delete.html",
        )

    def test_note_delete_view(self):
        response = self.client.post(
            reverse(
                "notes:note_delete",
                args=[self.note.pk],
            )
        )

        self.assertEqual(Note.objects.count(), 0)

        self.assertRedirects(
            response,
            reverse("notes:note_list"),
        )

    def test_invalid_note_returns_404(self):
        response = self.client.get(
            reverse(
                "notes:note_detail",
                args=[999],
            )
        )

        self.assertEqual(response.status_code, 404)


class NoteURLTest(TestCase):
    """Tests that the main URL patterns work."""

    def setUp(self):
        self.note = Note.objects.create(
            title="URL Test Note",
            content="Testing URLs.",
        )

    def test_note_list_url(self):
        response = self.client.get(
            reverse("notes:note_list")
        )

        self.assertEqual(response.status_code, 200)

    def test_note_create_url(self):
        response = self.client.get(
            reverse("notes:note_create")
        )

        self.assertEqual(response.status_code, 200)

    def test_note_detail_url(self):
        response = self.client.get(
            reverse(
                "notes:note_detail",
                args=[self.note.pk],
            )
        )

        self.assertEqual(response.status_code, 200)