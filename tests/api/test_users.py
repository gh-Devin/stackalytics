# Copyright (c) 2013 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from tests.api import test_api


class TestAPIUsers(test_api.TestAPI):

    def test_users_empty(self):
        with test_api.make_runtime_storage({}):
            response = self.app.get('/api/1.0/users')
            self.assertEqual(200, response.status_code)

    def test_users(self):
        with test_api.make_runtime_storage(
                {'repos': [{'module': 'nova', 'project_type': 'openstack',
                            'organization': 'openstack',
                            'uri': 'git://github.com/openstack/nova.git'}]},
                ['commit'],
                user_id=['john_doe', 'bill_smith']):
            response = self.app.get('/api/1.0/users')
            users = json.loads(response.data)['users']
            self.assertEqual(2, len(users))
            self.assertIn({'id': 'john_doe', 'text': 'John Doe'}, users)
            self.assertIn({'id': 'bill_smith', 'text': 'John Doe'}, users)

    def test_users_search(self):
        with test_api.make_runtime_storage(
                {'repos': [{'module': 'nova', 'project_type': 'openstack',
                            'organization': 'openstack',
                            'uri': 'git://github.com/openstack/nova.git'}]},
                ['commit'],
                user_name=['John Doe', 'Bill Smith']):
            response = self.app.get('/api/1.0/users?query=doe')
            users = json.loads(response.data)['users']
            self.assertEqual(1, len(users))
            self.assertIn({'id': 'john_doe', 'text': 'John Doe'}, users)

    def test_user_details(self):
        with test_api.make_runtime_storage(
                {'user:john_doe': {
                    'seq': 1, 'user_id': 'john_doe', 'user_name': 'John Doe',
                    'companies': [{'company_name': 'NEC', 'end_date': 0}],
                    'emails': 'john_doe@gmail.com'}}):
            response = self.app.get('/api/1.0/users/john_doe')
            user = json.loads(response.data)['user']
            self.assertEqual('john_doe', user['user_id'])

    def test_user_not_found(self):
        with test_api.make_runtime_storage(
                {'user:john_doe': {
                    'seq': 1, 'user_id': 'john_doe', 'user_name': 'John Doe',
                    'companies': [{'company_name': 'NEC', 'end_date': 0}],
                    'emails': 'john_doe@gmail.com'}}):
            response = self.app.get('/api/1.0/users/nonexistent')
            self.assertEqual(404, response.status_code)
