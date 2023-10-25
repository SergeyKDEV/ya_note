from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()
NOTES_COUNT = 20


class TestNotesPage(TestCase):
    NOTES_LIST_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Creator')
        Note.objects.bulk_create(
            Note(title=f'Note {index} title',
                 text=f'Note text.',
                 slug=f'note_{index}',
                 author=cls.author
                 )
            for index in range(NOTES_COUNT)
        )

    def list_url_response(self):
        return self.client.get(self.NOTES_LIST_URL)

    def test_all_notes_display(self):
        self.client.force_login(self.author)
        self.assertEqual(len(self.list_url_response().context['object_list']),
                         NOTES_COUNT,
                         f'На странице заметок отображены не все элементы.')
