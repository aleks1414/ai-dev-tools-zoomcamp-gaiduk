from django.test import TestCase, Client
from django.urls import reverse
from .models import Task

class TaskTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.task = Task.objects.create(title="Test Task", description="Test Desc", due_date="2025-12-31")

	def test_task_list(self):
		response = self.client.get(reverse('task_list'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.task.title)


	def test_create_task(self):
		response = self.client.post(reverse('task_create'), {
			'title': 'New Task',
			'description': 'New Desc',
			'due_date': '2025-12-25',
		})
		self.assertEqual(response.status_code, 302)  # Redirect after creation
		task = Task.objects.get(title='New Task')
		self.assertEqual(task.description, 'New Desc')
		self.assertEqual(str(task.due_date), '2025-12-25')

	def test_create_task_without_due_date(self):
		response = self.client.post(reverse('task_create'), {
			'title': 'No Due Date',
			'description': 'No due',
			'due_date': '',
		})
		self.assertEqual(response.status_code, 302)
		task = Task.objects.get(title='No Due Date')
		self.assertIsNone(task.due_date)

	def test_edit_task(self):
		response = self.client.post(reverse('task_edit', args=[self.task.id]), {
			'title': 'Updated Task',
			'description': 'Updated Desc',
			'due_date': '2025-12-30',
		})
		self.assertEqual(response.status_code, 302)
		self.task.refresh_from_db()
		self.assertEqual(self.task.title, 'Updated Task')
		self.assertEqual(self.task.description, 'Updated Desc')
		self.assertEqual(str(self.task.due_date), '2025-12-30')

	def test_edit_task_remove_due_date(self):
		response = self.client.post(reverse('task_edit', args=[self.task.id]), {
			'title': 'No Due Date',
			'description': 'No due',
			'due_date': '',
		})
		self.assertEqual(response.status_code, 302)
		self.task.refresh_from_db()
		self.assertIsNone(self.task.due_date)

	def test_delete_task(self):
		response = self.client.post(reverse('task_delete', args=[self.task.id]))
		self.assertEqual(response.status_code, 302)
		self.assertFalse(Task.objects.filter(id=self.task.id).exists())

	def test_complete_task(self):
		response = self.client.get(reverse('task_complete', args=[self.task.id]))
		self.assertEqual(response.status_code, 302)
		self.task.refresh_from_db()
		self.assertTrue(self.task.completed)
