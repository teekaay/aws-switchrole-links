from nose.tools import assert_equal
from aws_switchrole_links.utils import parse_arn

def test_parse_arn():
    arn = 'arn:aws:iam::1234:role/test'
    parsed_arn = parse_arn(arn)
    assert_equal(parsed_arn.get('account_id'), '1234')
