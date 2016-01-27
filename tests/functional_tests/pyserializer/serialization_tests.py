from nose.tools import *  # flake8: noqa
from mock import *  # flake8: noqa

from datetime import date, datetime
import json

from pyserializer.serializers import Serializer
from pyserializer import fields


class TestSerialization(object):

    def setup(self):
        class UserSerializer(Serializer):
            email = fields.CharField()
            username = fields.CharField()

            class Meta:
                fields = (
                    'email',
                    'username'
                )

        class CommentSerializer(Serializer):
            user = UserSerializer(source='user')
            content = fields.CharField()
            created_date = fields.DateField(format='%d/%m/%y')
            created_time = fields.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')

            class Meta:
                fields = (
                    'user',
                    'content',
                    'created_date',
                    'created_time'
                )

        class User(object):
            def __init__(self):
                self.email = 'foo@example.com'
                self.username = 'foobar'

        class Comment(object):
            def __init__(self):
                self.user = User()
                self.content = 'Some text content'
                self.created_date = date(2015, 1, 1)
                self.created_time = datetime(2015, 1, 1, 10, 30)

        self.UserSerializer = UserSerializer
        self.CommentSerializer = CommentSerializer
        self.user = User()
        self.comment = Comment()

    def test_simple_serialization(self):
        serializer = self.UserSerializer(self.user)
        expected_output = {
            "email": "foo@example.com",
            "username": "foobar"
        }
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json['email'], expected_output['email'])
        assert_equal(serialized_json['username'], expected_output['username'])

    def test_nested_serialization(self):
        serializer = self.CommentSerializer(self.comment)
        expected_output = {
            "user": {
                "email": "foo@example.com",
                "username": "foobar"
            },
            "content": "Some text content",
            "created_date": "01/01/15",
            "created_time": "2015-01-01T10:30:00Z"
        }
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(
            serialized_json['user']['email'], expected_output['user']['email']
        )
        assert_equal(
            serialized_json['user']['username'],
            expected_output['user']['username']
        )
        assert_equal(
            serialized_json['content'], expected_output['content']
        )
        assert_equal(
            serialized_json['created_date'], expected_output['created_date']
        )
        assert_equal(
            serialized_json['created_time'], expected_output['created_time']
        )
