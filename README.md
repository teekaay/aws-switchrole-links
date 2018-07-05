# aws-switchrole-links

[![Build Status](https://travis-ci.org/teekaay/aws-switchrole-links.svg?branch=master)](https://travis-ci.org/teekaay/aws-switchrole-links)

`aws-switchrole-links` is a simple script to generate links for easily switching
roles in the AWS console. It generates links that automatically fill
in the required fields so you only need to click a single button!

If you operate in a lot of different roles and accounts
or regularly clear your cookies, you may find this script useful.

## How it works

In the AWS console you can switch roles either by using the `Switch Role` link
in the upper right corner after clicking on your current profile OR directly
generate a link like
`https://signin.aws.amazon.com/switchrole?account=1234567890&roleName=admin&displayName=admin-profile&region=eu-central-1`.

which will switch to the role `admin` in account `1234567890` in `eu-central-1`
and display it as `admin-profile` (see `examples/awscli-config`).

## Installation

    git clone <repo> aws-switchrole-links
    cd aws-switchrole-links
    python setup.py install

or 
  
    pip install git+https://github.com/teekaay/aws-switchrole-links.git

to install the latest version from Github.

Make sure to have awscli installed (`pip install awscli`) and have configured
it.

## Usage

    usage: aws-switchrole-links [-h] [--config CONFIG] [--format {json,text}] [--verbose]

    optional arguments:
      -h, --help            show this help message and exit
      --config CONFIG       jmespath expression for filtering output
      --format {json,text}  output format
      --verbose             enable verbose logging

### Example

Basic usage
  
    $ aws-switchrole-links --format text --config examples/awscli-config
    admin-profile :: https://signin.aws.amazon.com/switchrole?region=eu-central-1&roleName=admin&displayName=admin-profile&account=1234567890

    $ aws-switchrole-links --format json --config examples/awscli-config
    {
        "signinLinks": [
            {
            "parameters": {
                "accountId": "1234567890",
                "roleName": "admin",
                "displayName": "admin-profile",
                "region": "eu-central-1"
            },
            "displayName": "admin-profile",
            "signinUrl": "https://signin.aws.amazon.com/switchrole?region=eu-central-1&roleName=admin&displayName=admin-profile&account=1234567890"
            }
        ]
    }
