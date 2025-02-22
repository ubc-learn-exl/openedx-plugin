"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Aug-2021

Tests of the openedx_plugin_api
"""
from django.urls import reverse
from rest_framework.test import APITestCase

from xmodule.modulestore.tests.django_utils import SharedModuleStoreTestCase


class TestAPIEndpoints(SharedModuleStoreTestCase, APITestCase):
    """
    Extremely basic Tests.
    Try each url end point, assert that it returns a 200 response code.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # hook for future use.

    def setUp(self):
        super().setUp()

        self.response = self.client.get(reverse("openedx_plugin/api/edxapi_meta"))
        assert self.response.status_code == 200
