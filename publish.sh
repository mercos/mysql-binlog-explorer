#!/usr/bin/env bash
set -e

VERSION=$(cat binlogexplorer/version)

STATUS_CODE=$(curl --write-out %{http_code} --silent --output /dev/null https://pypi.org/project/mysql-binlog-explorer/$V{ERSION}/)

https://pypi.org/project/mysql-binlog-explorer/0.2.3/
if [[ ${STATUS_CODE } = "200" ]]; then
  echo "Version '${VERSION}' already published. Did you forget to update the version code?"
  exit 1
fi

echo 'Preparing dist dir...'
python setup.py sdist

echo 'Testing distribution and installation...'
twine upload --repository-url https://test.pypi.org/legacy/ dist/mysql-binlog-explorer-${VERSION}.tar.gz --skip-existing -u ${TEST_PYPI_USER} -p ${TEST_PYPI_PASSWORD}
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple mysql-binlog-explorer
mysql-binlog-explorer -h

echo 'Publishing on PyPi'
twine upload dist/mysql-binlog-explorer-${VERSION}.tar.gz -u ${PYPI_USER} -p ${PYPI_PASSWORD}
