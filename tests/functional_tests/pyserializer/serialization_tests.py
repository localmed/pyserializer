from nose.tools import *  # flake8: noqa
from mock import *  # flake8: noqa

from datetime import date, datetime
import json

from pyserializer.serializers import Serializer
from pyserializer import fields


class TestNestsedSerialization:

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

        class User:
            def __init__(self):
                self.email = 'foo@example.com'
                self.username = 'foobar'

        class Comment:
            def __init__(self):
                self.user = User()
                self.content = 'Some text content'
                self.created_date = date(2015, 1, 1)
                self.created_time = datetime(2015, 1, 1, 10, 30)

        self.UserSerializer = UserSerializer
        self.CommentSerializer = CommentSerializer
        self.user = User()
        self.comment = Comment()
        self.Comment = Comment

    def test_simple_serialization(self):
        serializer = self.UserSerializer(self.user)
        expected_output = {
            'email': 'foo@example.com',
            'username': 'foobar'
        }
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json['email'], expected_output['email'])
        assert_equal(serialized_json['username'], expected_output['username'])

    def test_nested_serialization(self):
        serializer = self.CommentSerializer(self.comment)
        expected_output = {
            'user': {
                'email': 'foo@example.com',
                'username': 'foobar'
            },
            'content': 'Some text content',
            'created_date': '01/01/15',
            'created_time': '2015-01-01T10:30:00Z'
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

    def test_mutliple_serializers(self):
        serializer_1 = self.CommentSerializer(self.comment)
        serialized_json_1 = json.loads(json.dumps(serializer_1.data))
        assert_equal(serialized_json_1['user']['email'], 'foo@example.com')
        comment_2 = self.Comment()
        comment_2.content = 'some new content'
        comment_2.user.email = 'foo2@example.com'
        serializer_2 = self.CommentSerializer(comment_2)
        serialized_json_2 = json.loads(json.dumps(serializer_2.data))
        assert_equal(serialized_json_2['user']['email'], 'foo2@example.com')
        assert_equal(serialized_json_2['content'], 'some new content')


class TestSerializationWithManyTrue:

    def setup(self):
        class UserSerializer(Serializer):
            email = fields.CharField()
            username = fields.CharField()

            class Meta:
                fields = (
                    'email',
                    'username'
                )

        class User:
            def __init__(self, email, username):
                self.email = email
                self.username = username

        self.UserSerializer = UserSerializer
        self.user_1 = User(
            email='foo_1@bar.com',
            username='foo_1'
        )
        self.user_2 = User(
            email='foo_2@bar.com',
            username='foo_2'
        )
        self.users = [self.user_1, self.user_2]

    def test_simple_serialization(self):
        serializer = self.UserSerializer(self.users, many=True)
        expected_output = [{
            'username': 'foo_1',
            'email': 'foo_1@bar.com'
        }, {
            'username': 'foo_2',
            'email': 'foo_2@bar.com'
        }]
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json, expected_output)


class TestSerializationWithNestedSource:

    def setup(self):
        class LocationSerializer(Serializer):
            street = fields.CharField()
            state = fields.CharField()

            class Meta:
                fields = (
                    'street',
                    'state'
                )

        class CommentSerializer(Serializer):
            content = fields.CharField()
            location = LocationSerializer(source='user.location')

            class Meta:
                fields = (
                    'content',
                    'location',
                )

        class Location:
            def __init__(self):
                self.street = 'Street 123'
                self.state = 'LA'

        class User:
            def __init__(self):
                self.location = Location()

        class Comment:
            def __init__(self):
                self.user = User()
                self.content = 'Some text content'

        self.CommentSerializer = CommentSerializer
        self.user = User()
        self.comment = Comment()

    def test_serialization_with_nested_source(self):
        serializer = self.CommentSerializer(self.comment)
        expected_output = {
            'content': 'Some text content',
            'location': {
                'state': 'LA',
                'street': 'Street 123'
            }
        }
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json, expected_output)
