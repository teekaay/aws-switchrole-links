#!/usr/bin/env python

"""
A simple script to generate AWS console links for quickly switching roles
based on the profiles in the AWS CLI configuration.
"""

import configparser
import logging
import argparse
import pathlib
import json
import sys

logger = logging.getLogger(__name__)

AWS_SIGNIN_BASE_URL = 'https://signin.aws.amazon.com'
AWS_CLI_CONFIG = '%s/.aws/config' %(pathlib.Path.home())
OUTPUT_FORMATS = (
    JSON, TEXT
) = (
    'json', 'text'
)

def parse_arn(arn):
    parts = arn.split(':')
    sections = {
        'owner': parts[1],
        'service': parts[2],
        'region': parts[3],
        'account_id': parts[4],
        'resource': parts[5]
    }
    return sections

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='create switchrole links for AWS console')
    arg_parser.add_argument('--format', help='the output format', choices=OUTPUT_FORMATS, default=TEXT)
    arg_parser.add_argument('--config', help='path to the aws cli config file. defaults to %s' %(AWS_CLI_CONFIG), default=AWS_CLI_CONFIG)
    arg_parser.add_argument('--out', help='path to destination file. if not set, will print to stdout')
    arg_parser.add_argument('--verbose', help='enable verbose logging', action='store_true')

    args = arg_parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if not pathlib.Path(args.config).is_file():
        logger.error('configuration files [%s] does not exists. exiting', args.config)
        sys.exit(-1)

    config = configparser.ConfigParser()
    logger.debug('reading configuration from [%s]', args.config)
    config.read(args.config)

    switch_role_links = []

    for section_name in config.sections():
        section = config[section_name]
        if section.get('role_arn'):
            arn = parse_arn(section.get('role_arn'))
            role_name = arn['resource'].replace('role/', '')
            account_id = arn['account_id']
            display_name = section_name.replace('profile ', '')
            region = section['region']
            url = '%s/switchrole?account=%s&roleName=%s&displayName=%s&region=%s' %(AWS_SIGNIN_BASE_URL, account_id, role_name, display_name, region)
            switch_role_data = {
                'profile': section_name,
                'url': url
            }
            switch_role_links.append(switch_role_data)
        else:
            logger.debug('profile [%s] has no role_arn attribute, skipping it', section_name)

    output = ''

    if args.format == JSON:
        out_json = { 'links': switch_role_links }
        output = json.dumps(out_json, sort_keys=True, indent=2)
    elif args.format == TEXT:
        lines = []
        for link in switch_role_links:
            line = '%s: %s' %(link['profile'], link['url'])
            lines.append(line)
        output = '\n'.join(lines)
    else:
        raise Exception('unknown output format %s' %(args.format))

    if args.out:
        with open(args.out, 'w') as outf:
            outf.write(output)
    else:
        print(output)
