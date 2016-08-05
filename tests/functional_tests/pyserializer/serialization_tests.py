from nose.tools import *  # flake8: noqa
from mock import *  # flake8: noqa

from datetime import date, datetime
import json

from pyserializer.serializers import Serializer
from pyserializer import fields


class TestSimpleSerialization:

    def setup(self):
        class UserSerializer(Serializer):
            email = fields.CharField()
            username = fields.CharField()

        class User:
            def __init__(self,
                         email='foo@example.com',
                         username='foobar'):
                self.email = email
                self.username = username

        self.User = User
        self.UserSerializer = UserSerializer

    def test_simple_serialization(self):
        user = self.User()
        serializer = self.UserSerializer(user)
        expected_output = {
            'email': 'foo@example.com',
            'username': 'foobar'
        }
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json['email'], expected_output['email'])
        assert_equal(serialized_json['username'], expected_output['username'])


class TestSimpleSerializationWithMetaFields:

    def setup(self):
        class UserSerializer(Serializer):
            email = fields.CharField()
            username = fields.CharField()

            class Meta:
                fields = (
                    'email',
                )

        class User:
            def __init__(self,
                         email='foo@example.com',
                         username='foobar'):
                self.email = email
                self.username = username

        self.User = User
        self.UserSerializer = UserSerializer

    def test_simple_serialization_with_meta_fields(self):
        user = self.User()
        serializer = self.UserSerializer(user)
        expected_output = {
            'email': 'foo@example.com',
        }
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json['email'], expected_output['email'])
        assert_equal(list(serialized_json.keys()), ['email'])


class TestSimpleSerializationWithMetaExclude:

    def setup(self):
        class UserSerializer(Serializer):
            email = fields.CharField()
            username = fields.CharField()

            class Meta:
                exclude = (
                    'username',
                )

        class User:
            def __init__(self,
                         email='foo@example.com',
                         username='foobar'):
                self.email = email
                self.username = username

        self.User = User
        self.UserSerializer = UserSerializer

    def test_simple_serialization_with_meta_exclude(self):
        user = self.User()
        serializer = self.UserSerializer(user)
        expected_output = {
            'email': 'foo@example.com',
        }
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json['email'], expected_output['email'])
        assert_equal(list(serialized_json.keys()), ['email'])


class TestSerializationWithSourceSpecifiedOnField:

    def setup(self):
        class UserSerializer(Serializer):
            username = fields.CharField()
            createdAt = fields.DateTimeField(
                source='created_at',
                format='%Y-%m-%dT%H:%M:%SZ'
            )

            class Meta:
                fields = (
                    'username',
                    'createdAt'
                )

        class User:
            def __init__(self,
                         username='foobar',
                         created_at=datetime(2015, 1, 1, 10, 30)):
                self.username = username
                self.created_at = created_at

        self.User = User
        self.UserSerializer = UserSerializer

    def test_serialization_with_source_on_field(self):
        user = self.User()
        serializer = self.UserSerializer(user)
        expected_output = {
            'username': 'foobar',
            'createdAt': '2015-01-01T10:30:00Z'
        }
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json, expected_output)


class TestNestsedSerialization:

    def setup(self):
        class UserSerializer(Serializer):
            email = fields.CharField()
            username = fields.CharField()

        class CommentSerializer(Serializer):
            user = UserSerializer(source='user')
            content = fields.CharField()
            created_date = fields.DateField(format='%d/%m/%y')
            created_time = fields.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')

        class User:
            def __init__(self,
                         email='foo@example.com',
                         username='foobar'):
                self.email = email
                self.username = username

        class Comment:
            def __init__(self,
                         user,
                         content='Some text content',
                         create_date=date(2015, 1, 1),
                         created_time=datetime(2015, 1, 1, 10, 30)):
                self.user = user
                self.content = 'Some text content'
                self.created_date = date(2015, 1, 1)
                self.created_time = datetime(2015, 1, 1, 10, 30)

        self.UserSerializer = UserSerializer
        self.CommentSerializer = CommentSerializer
        self.User = User
        self.Comment = Comment

    def test_nested_serialization(self):
        comment = self.Comment(user=self.User())
        serializer = self.CommentSerializer(comment)
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
        comment = self.Comment(user=self.User())
        serializer_1 = self.CommentSerializer(comment)
        serialized_json_1 = json.loads(json.dumps(serializer_1.data))
        assert_equal(serialized_json_1['user']['email'], 'foo@example.com')
        comment_2 = self.Comment(user=self.User())
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

    def test_simple_serialization_with_many_true(self):
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


class TestSerializationWithNestedSourceDefined:

    def setup(self):
        class LocationSerializer(Serializer):
            street = fields.CharField()
            state = fields.CharField()

        class CommentSerializer(Serializer):
            content = fields.CharField()
            location = LocationSerializer(source='user.location')

        class Location:
            def __init__(self, street='Street 123', state='LA'):
                self.street = street
                self.state = state

        class User:
            def __init__(self, location):
                self.location = location

        class Comment:
            def __init__(self, user, content='Some text content'):
                self.user = user
                self.content = content

        self.CommentSerializer = CommentSerializer
        self.Location = Location
        self.User = User
        self.Comment = Comment

    def test_serialization_with_nested_source(self):
        location = self.Location()
        user = self.User(location=location)
        comment = self.Comment(user=user)
        serializer = self.CommentSerializer(comment)
        expected_output = {
            'content': 'Some text content',
            'location': {
                'state': 'LA',
                'street': 'Street 123'
            }
        }
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json, expected_output)


class TestSerializationWithAllowBlankSource:

    def setup(self):
        class LocationSerializer(Serializer):
            street = fields.CharField()
            state = fields.CharField()

        class CommentSerializer(Serializer):
            content = fields.CharField()
            location = LocationSerializer(
                source='user.location',
                allow_blank_source=True
            )

        class Location:
            def __init__(self, street='Street 123', state='LA'):
                self.street = street
                self.state = state

        class User:
            def __init__(self, location):
                self.location = location

        class Comment:
            def __init__(self, user, content='Some text content'):
                self.user = user
                self.content = content

        self.CommentSerializer = CommentSerializer
        self.Location = Location
        self.User = User
        self.Comment = Comment

    def test_serializer_when_nested_obj_is_none(self):
        user = None
        comment = self.Comment(user=user)
        serializer = self.CommentSerializer(comment)
        expected_output = {
            'content': 'Some text content',
            'location': None
        }
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json, expected_output)


class TestSerializationWithAllowBlankSourceAndManyTrue:

    def setup(self):
        class AddressSerializer(Serializer):
            street = fields.CharField()
            state = fields.CharField()

        class UserSerializer(Serializer):
            username = fields.CharField()
            address = AddressSerializer(
                source='address',
                many=True,
                allow_blank_source=True
            )

        class User:
            def __init__(self, address, username='foobar'):
                self.address = address
                self.username = username

        self.UserSerializer = UserSerializer
        self.User = User

    def test_serializer_when_nested_obj_is_none(self):
        user = self.User(address=[None])
        serializer = self.UserSerializer(user)
        expected_output = {
            'username': 'foobar',
            'address': []
        }
        serialized_json = json.loads(json.dumps(serializer.data))
        assert_equal(serialized_json, expected_output)
