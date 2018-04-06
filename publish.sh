#!/usr/bin/env bash
set -e

version=$(cat version)
statusCode=$(curl --write-out %{http_code} --silent \
                  --output /dev/null https://pypi.python.org/pypi/mysql-binlog-explorer/${version})

if [[ ${statusCode} = "200" ]]; then
  echo "Version '${version}' already published. Did you forget to update the version code?"
  exit 1
fi

echo 'Preparing dist dir...'
rm -rf dist/*
python setup.py sdist

echo 'Testing distribution and installation...'
pip uninstall mysql-binlog-explorer -y || true
twine upload --repository-url https://test.pypi.org/legacy/ dist/mysql-binlog-explorer-${version}.tar.gz \
        --skip-existing -u ${TEST_PYPI_USER} -p ${TEST_PYPI_PASSWORD}
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple mysql-binlog-explorer
mysql-binlog-explorer -h

echo 'Publishing on PyPi'
twine upload dist/mysql-binlog-explorer-${version}.tar.gz -u ${PYPI_USER} -p ${PYPI_PASSWORD}
