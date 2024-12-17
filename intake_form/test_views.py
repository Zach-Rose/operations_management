# intake_form/test_views.py
from django.test import TestCase
from django.urls import reverse
from .models import Process
from .forms import ProcessForm


class SubmitIntakeFormTest(TestCase):
    def test_submit_intake_form_get(self):
        response = self.client.get(reverse('submit_intake_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'intake_form/submit_form.html')
        self.assertIsInstance(response.context['form'], ProcessForm)

    def test_submit_intake_form_post(self):
        data = {
            'name': 'Test Process',
            'description': 'This is a test process.',
            'ideal_duration': '1 00:00:00',  # 1 day
            'steps': []  # Assuming steps can be empty for this test
        }
        response = self.client.post(reverse('submit_intake_form'), data)
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertTrue(Process.objects.filter(name='Test Process').exists())
