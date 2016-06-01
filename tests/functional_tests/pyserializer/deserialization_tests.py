from nose.tools import *  # flake8: noqa
from mock import *  # flake8: noqa

from datetime import date, datetime

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
        obj = deserializer.object
        assert_equal(obj.user.email, 'foo@example.com')
        assert_equal(obj.user.username, 'JohnSmith')
        assert_equal(obj.content, 'foo bar')
        assert_equal(obj.created_date, date(2015, 1, 1))
        assert_equal(obj.created_time, datetime(2012, 1, 1, 16, 0))


class TestMultipleNestedDeserialization(object):

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
            content = fields.CharField()
            commented_at = fields.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')

            class Meta:
                fields = (
                    'content',
                    'commented_at',
                )

            def __repr__(self):
                return '<Comment(%r)>' % (self.content)

        class PostDeserializer(Serializer):
            user = UserDeserializer()
            comment = CommentDeserializer()
            posted_at = fields.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')

            class Meta:
                fields = (
                    'user',
                    'comment',
                    'posted_at',
                )

            def __repr__(self):
                return '<PostDeserializer(%r)>' % (self.user.username)

        self.PostDeserializer = PostDeserializer

    def test_multiple_nested_deserialization(self):
        post_data = {
            'user': {
                'email': 'foo@example.com',
                'username': 'JohnSmith'
            },
            'comment': {
                'content': 'foo bar',
                'commented_at': '2012-01-01T16:00:00Z'
            },
            'posted_at': '2012-01-01T16:00:00Z'
        }
        deserializer = self.PostDeserializer(data_dict=post_data)
        obj = deserializer.object
        assert_equal(obj.user.email, 'foo@example.com')
        assert_equal(obj.user.username, 'JohnSmith')
        assert_equal(obj.comment.content, 'foo bar')
        assert_equal(obj.comment.commented_at, datetime(2012, 1, 1, 16, 0))
        assert_equal(obj.posted_at, datetime(2012, 1, 1, 16, 0))


class TestInternalNestedDeserialization(object):

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
            commented_at = fields.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')

            class Meta:
                fields = (
                    'user',
                    'content',
                    'commented_at',
                )

            def __repr__(self):
                return '<Comment(%r)>' % (self.content)

        class PostDeserializer(Serializer):
            comment = CommentDeserializer()
            posted_at = fields.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')

            class Meta:
                fields = (
                    'comment',
                    'posted_at',
                )

            def __repr__(self):
                return '<PostDeserializer(%r)>' % (self.user.username)

        self.PostDeserializer = PostDeserializer

    def test_multiple_nested_deserialization(self):
        post_data = {
            'comment': {
                'content': 'foo bar',
                'commented_at': '2012-01-01T16:00:00Z',
                'user': {
                    'email': 'foo@example.com',
                    'username': 'JohnSmith'
                }
            },
            'posted_at': '2012-01-01T16:00:00Z'
        }
        deserializer = self.PostDeserializer(data_dict=post_data)
        obj = deserializer.object
        assert_equal(obj.comment.content, 'foo bar')
        assert_equal(obj.comment.commented_at, datetime(2012, 1, 1, 16, 0))
        assert_equal(obj.comment.user.email, 'foo@example.com')
        assert_equal(obj.comment.user.username, 'JohnSmith')
        assert_equal(obj.posted_at, datetime(2012, 1, 1, 16, 0))
