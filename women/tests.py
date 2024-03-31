from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

class GetPagesTestCase(TestCase):
    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('women/index.html', response.template_name)
        self.assertEqual(response.context_data['title'], 'Главная страница')
        
    def test_redirect_addpage(self):
        path = reverse('add_page')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)