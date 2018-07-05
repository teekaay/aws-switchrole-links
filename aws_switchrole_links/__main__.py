#!/usr/bin/env python

import argparse
import json
import logging
import configparser
import os
import sys
from pathlib import Path

from aws_switchrole_links.utils import parse_arn

LOG = logging.getLogger('aws_switchrole_links.cli')
AWS_CLI_CONFIG = os.path.join(str(Path.home()), '.aws', 'config')
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
        help='path to aws config file')
    parser.add_argument('--format', type=str, choices=OUTPUT_FORMATS, default=TEXT,
        help='output format')
    parser.add_argument('--verbose', action='store_true',
        help='enable verbose logging')

    args = parser.parse_args()

    init_logging(verbose=args.verbose)

    aws_config = configparser.ConfigParser()
    LOG.debug('reading aws configuration from [%s]', args.config)
    aws_config.read(args.config)
    aws_config['DEFAULTS'] = aws_config['default']

    links = []

    for section in aws_config.sections():
        profile = aws_config[section]
        if section == 'default':
            continue

        if profile.get('role_arn') is None:
            continue

        region = profile.get('region')
        display_name = section.replace('profile ', '')
        role_arn = profile.get('role_arn')
        arn_parts = parse_arn(role_arn)
        role_name = arn_parts.get('resource').replace('role/', '')
        account_id = arn_parts.get('account_id')

        profile['roleName'] = role_name
        profile['accountId'] = account_id

        parameters = {
            'accountId': account_id,
            'roleName': role_name,
            'region': region,
            'displayName': display_name
        }
        signin_url = 'https://signin.aws.amazon.com/switchrole?region={region}&roleName={roleName}&displayName={displayName}&account={accountId}'.format(**parameters)

        item = {
            'signinUrl': signin_url,
            'displayName': display_name,
            'parameters': parameters
        }        
        links.append(item)

    final_result = {
        'signinLinks': links
    }

    if args.format == JSON:
        print(json.dumps(final_result, indent=2))
    elif args.format == TEXT:
        links_to_print = []
        for link in final_result.get('signinLinks'):
            print('%s :: %s' %(link.get('displayName'), link.get('signinUrl')))
    else:
        LOG.error('invalid format [%s]', args.format)
        sys.exit(1)

if __name__ == '__main__':
    main()
