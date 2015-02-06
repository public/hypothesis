set -o xtrace -e

if [ -z $1 ]; then
    CURRENT_PYTHON=$(which python)
else
    CURRENT_PYTHON=$(which $1);
fi

VENV=$(mktemp -d)

rm -rf ./dist
virtualenv $VENV  --python=$CURRENT_PYTHON
BINDIR=$VENV/bin
export PYTHON=$BINDIR/python

CURRENT_VERSION=$($CURRENT_PYTHON --version 2>&1)
VENV_VERSION=$($PYTHON --version 2>&1)

if [ "$CURRENT_VERSION" != "$VENV_VERSION" ]
then
  exit 1
fi

export PIP=$BINDIR/pip

$PIP install pytest coverage

PYTHONPATH=src $PYTHON -u -m coverage run -a --branch \
    --include 'src/hypothesis/*' \
    --omit 'src/hypothesis/settings.py,src/hypothesis/internal/compat.py' \
    -m pytest -v tests --ignore=tests/test_recursively.py
./ci/database-test.sh
coverage report -m --fail-under=100
PYTHONPATH=src $PYTHON -m pytest -v tests/test_recursively.py
pip install flake8 restructuredtext_lint pygments pyformat
find src tests -name "*.py" | xargs pyformat -i
git diff --exit-code
flake8 src tests --exclude=compat.py
rst-lint README.rst
$PIP uninstall pytest coverage -y
./ci/installer-test.sh
