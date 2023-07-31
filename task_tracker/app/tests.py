from django.test import TestCase
from django.db.utils import IntegrityError
from django.urls import reverse
from django.utils.timezone import now

from .models import *


class TaskMemberCreation(TestCase):
    _user: User

    @classmethod
    def setUpTestData(cls):
        cls._user = User.objects.create_user(id=1, username='assam', email='assam@hop.wey', password='somepassword')

    def test_happy_path(self):
        task_member = TaskMember(user=self._user, position='Head of security')
        task_member.save()
        self.assertTrue(task_member.id is not None)
        self.assertIs(task_member.position, 'Head of security')
        self.assertIs(task_member.user, self._user)

    def test_no_user_task_member(self):
        self.assertRaises(IntegrityError, TaskMember(user=None, position='Tester').save)

    def test_no_position(self):
        tm = TaskMember(user=self._user)
        tm.save()
        self.assertTrue(tm.id is not None)
        self.assertIs(tm.position, '')
        self.assertIs(tm.user, self._user)


class TaskViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls._user = User.objects.create_user(id=1, username='assam', email='assam@hop.wey', password='somepassword')
        tm = TaskMember(user=cls._user, position='position')
        tm.save()
        cls._tm = tm

    def test_happy_path(self):
        new_task = {
            'created_by': self._tm,
            'assigned_to': self._tm,
            'status': 'INIT',
            'created': now(),
            'estimate': 10,
            'name': 'Test task',
            'description': 'A task created for happy path'
        }
        t = Task(**new_task)
        t.save()
        url = reverse('app:task_details', args=(1,))
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_no_task_with_id(self):
        url = reverse('app:task_details', args=(2,))
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)
