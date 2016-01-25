from nose.tools import *  # flake8: noqa
from mock import *  # flake8: noqa

from datetime import date, datetime
import json

from pyserializer.serializers import Serializer
from pyserializer import fields


class TestDeserialization(object):

    def setup(self):
        class UserDeserializer(Serializer):
            email = fields.CharField()
            username = fields.CharField()

            class Meta:
                fields = (
                    'email',
                    'username'
                )

            def __repr__(self):
                return '<User(%r)>' % (self.username)

        self.UserDeserializer = UserDeserializer

    def test_deserialization(self):
        input_data = {
            'email': 'foo@example.com',
            'username': 'JohnSmith'
        }
        deserializer = self.UserDeserializer(data_dict=input_data)
        assert_equal(deserializer.object.email, input_data['email'])
        assert_equal(deserializer.object.username, input_data['username'])


class TestNestedDeserialization(object):

    def setup(self):
        class UserDeserializer(Serializer):
            email = fields.CharField()
            username = fields.CharField()

            class Meta:
                fields = (
                    'email',
                    'username'
                )

            def __repr__(self):
                return '<User(%r)>' % (self.username)

        class CommentDeserializer(Serializer):
            user = UserDeserializer()
            content = fields.CharField()
            created_date = fields.DateField(format='%Y-%m-%d')
            created_time = fields.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')

            class Meta:
                fields = (
                    'user',
                    'content',
                    'created_date',
                    'created_time',
                )

            def __repr__(self):
                return '<Comment(%r)>' % (self.content)

        self.UserDeserializer = UserDeserializer
        self.CommentDeserializer = CommentDeserializer

    def test_nested_deserialization(self):
        input_data = {
            'user': {
                'email': 'foo@example.com',
                'username': 'JohnSmith'
            },
            'content': 'foo bar',
            'created_date': '2015-01-01',
            'created_time': '2012-01-01T16:00:00Z'
        }
        deserializer = self.CommentDeserializer(data_dict=input_data)
        set_trace()
        assert_equal(
            deserializer.object.user.email,
            input_data['user']['email']
        )
        assert_equal(
            deserializer.object.user.username,
            input_data['user']['username']
        )
        assert_equal(
            deserializer.object.content,
            input_data['content']
        )
        assert_equal(
            deserializer.object.created_date,
            date(2015, 1, 1)
        )
        assert_equal(
            deserializer.object.created_time,
            datetime(2012, 1, 1, 16, 0)
        )
