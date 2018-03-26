#!/usr/bin/env python

import argparse
import json
import logging
import configparser
import os
import sys
import jmespath
from pathlib import Path

from aws_switchrole_links.utils import parse_arn

LOG = logging.getLogger('aws_switchrole_links.cli')
AWS_CLI_CONFIG = '%s/.aws/config' %(Path.home())
AWS_SIGNIN_BASE_URL = 'signin.aws.amazon.com'
OUTPUT_FORMATS = (
    JSON, TEXT
) = (
    'json', 'text'
)

def init_logging(verbose=False):
    log_level = logging.INFO
    if verbose:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level, format='%(asctime)-8s [%(levelname)s] %(message)s')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default=AWS_CLI_CONFIG,
        help='jmespath expression for filtering output')
    parser.add_argument('--query', type=str,
        help='jmespath expression for filtering output. only used when output format is json')
    parser.add_argument('--format', type=str, choices=OUTPUT_FORMATS, default=TEXT,
        help='output format')
    parser.add_argument('--verbose', action='store_true',
        help='enable verbose logging')

    args = parser.parse_args()

    init_logging(verbose=args.verbose)

    aws_config = configparser.ConfigParser()
    LOG.debug('reading aws configuration from [%s]', args.config)
    aws_config.read(args.config)

    default_settings = {
        'region': os.environ.get('AWS_REGION', 'us-east-1')
    }

    if 'default' in aws_config.sections():
        default_settings.update(dict(aws_config['default']))

    links = []

    for section in aws_config.sections():
        profile = dict(aws_config[section])
        if section == 'default':
            continue

        if profile.get('role_arn') is None:
            continue

        region = profile.get('region', default_settings['region'])
        profile_name = section.replace('profile ', '')
        role_arn = profile.get('role_arn')
        arn_parts = parse_arn(role_arn)
        role_name = arn_parts.get('resource').replace('role/', '')
        account_id = arn_parts.get('account_id')
        if arn_parts.get('region'):
            region = arn_parts.get('region')
        link = 'https://%s/switchrole?region=%s&roleName=%s&displayName=%s&account=%s' %(
            AWS_SIGNIN_BASE_URL, region, role_name, profile_name, account_id)

        profile['role_name'] = role_name
        profile['account_id'] = account_id

        item = {
            'link': link,
            'profile_name': profile_name,
            'profile': profile
        }
        links.append(item)

    final_result = {
        'links': links
    }

    if args.query:
        try:
            final_result = jmespath.search(args.query, final_result)
        except jmespath.exceptions.ParseError as e:
            LOG.error('failed to parse query [%s]: %s', args.query, e)
            sys.exit(1)

    if args.format == JSON:
        print(json.dumps(final_result, indent=2))
    elif args.format == TEXT:
        links_to_print = []
        # heuristic is: if query is set, then it must be the list final_result.links
        if args.query:
            links_to_print = final_result
        else:
            links_to_print = final_result.get('links')

        for link in links_to_print:
            print('profile %s: %s' %(link.get('profile_name'), link.get('link')))
    else:
        LOG.error('invalid format [%s]', args.format)
        sys.exit(1)

if __name__ == '__main__':
    main()
