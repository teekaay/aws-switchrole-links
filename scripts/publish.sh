#!/usr/bin/env bash

set -e

PYPI_REGISTRY="${PYPI_REGISTRY:-pypi}"

echo "Uploading to [$PYPI_REGISTRY]"

python setup.py sdist

twine upload \
    dist/* \
    -u $PYPI_USER \
    -p $PYPI_PASSWORD \
    -r $PYPI_REGISTRY

