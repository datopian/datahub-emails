import os
import unittest
import requests_mock

from datahub_emails import api


class TestStatusPage(unittest.TestCase):

    @requests_mock.mock()
    def test_on_incident_returns_none_if_comonent_not_exists(self, m):
        m.get('https://api.statuspage.io/v1/pages/test/components', json={})
        res = api.on_incident('Test Incident', 'testing')
        self.assertIsNone(res)

    @requests_mock.mock()
    def test_on_incident_works(self, m):
        m.get('https://api.statuspage.io/v1/pages/test/components', json=[{'name': 'test', 'id': 'test'}])
        m.post('https://api.statuspage.io/v1/pages/test/incidents', json={'success': True})
        res = api.on_incident('Test Incident', 'test', 'errors')
        self.assertDictEqual(res, {'success': True})

    @requests_mock.mock()
    def test_subscribe_user_returns_none_if_comonent_not_exists(self, m):
        m.get('https://api.statuspage.io/v1/pages/test/components', json={})
        res = api.subscribe_user('test', 'testing@mail.com')
        self.assertIsNone(res)

    @requests_mock.mock()
    def test_subscribe_user_works(self, m):
        m.get('https://api.statuspage.io/v1/pages/test/components', json=[{'name': 'test', 'id': 'test'}])
        m.post('https://api.statuspage.io/v1/pages/test/subscribers', json={'success': True})
        res = api.subscribe_user('test', 'testing@mail.com')
        self.assertDictEqual(res, {'success': True})
