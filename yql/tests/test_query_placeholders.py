"""Set of tests for the placeholder checking"""

from unittest import TestCase

from nose.tools import raises

import yql


class PublicTest(TestCase):
    @raises(ValueError)
    def test_empty_args_raises_valueerror(self):
        y = yql.Public()
        query = "SELECT * from foo where dog=@dog"
        params = {}
        y.execute(query, params)

    @raises(ValueError)
    def test_incorrect_args_raises_valueerror(self):
        y = yql.Public()
        query = "SELECT * from foo where dog=@dog"
        params = {'test': 'fail'}
        y.execute(query, params)

    @raises(ValueError)
    def test_params_raises_when_not_dict(self):
        y = yql.Public()
        query = "SELECT * from foo where dog=@dog"
        params = ['test']
        y.execute(query, params)

    @raises(ValueError)
    def test_unecessary_args_raises_valueerror(self):
        y = yql.Public()
        query = "SELECT * from foo where dog='test'"
        params = {'test': 'fail'}
        y.execute(query, params)

    @raises(ValueError)
    def test_incorrect_type_raises_valueerror(self):
        y = yql.Public()
        query = "SELECT * from foo where dog=@test"
        params = ('fail')
        y.execute(query, params)

    def test_placeholder_regex_one(self):
        query = yql.YQLQuery("SELECT * from foo where email='foo@foo.com'")
        placeholders = query.get_placeholder_keys()
        self.assertEqual(placeholders, [])

    def test_placeholder_regex_two(self):
        query = yql.YQLQuery("SELECT * from foo where email=@foo'")
        placeholders = query.get_placeholder_keys()
        self.assertEqual(placeholders, ['foo'])

    def test_placeholder_regex_three(self):
        query = yql.YQLQuery("SELECT * from foo where email=@foo and test=@bar'")
        placeholders = query.get_placeholder_keys()
        self.assertEqual(placeholders, ['foo', 'bar'])

    def test_placeholder_regex_four(self):
        query = yql.YQLQuery("SELECT * from foo where foo='bar' LIMIT @foo")
        placeholders = query.get_placeholder_keys()
        self.assertEqual(placeholders, ['foo'])

    def test_placeholder_regex_five(self):
        query = yql.YQLQuery("""SELECT * from foo
                    where foo='bar' LIMIT
                    @foo""")
        placeholders = query.get_placeholder_keys()
        self.assertEqual(placeholders, ['foo'])

