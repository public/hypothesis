set -o xtrace -e

export HYPOTHESIS_DATABASE_FILE=$(mktemp --suffix=.db)
PYTHONPATH=src $PYTHON -u -m coverage run -a --branch \
    --include 'src/hypothesis/*' \
    --omit 'src/hypothesis/settings.py,src/hypothesis/internal/compat.py'\
    -m pytest -v tests --ignore=tests/test_recursively.py
PYTHONPATH=src $PYTHON -c '
from __future__ import print_function

from hypothesis.database import ExampleDatabase
from hypothesis.database.backend import SQLiteBackend
import os
import sys
database_file = os.getenv("HYPOTHESIS_DATABASE_FILE")
print("Database file is", database_file)

db = ExampleDatabase(
    backend=SQLiteBackend(database_file))
data = list(db.storage_for((((int,), {}),)).fetch())
if not data:
    print("No integer examples in database")
    sys.exit(1)
'
PYTHONPATH=src $PYTHON -u -m coverage run -a --branch \
    --include 'src/hypothesis/*' \
    --omit 'src/hypothesis/settings.py,src/hypothesis/internal/compat.py'\
    -m pytest -v tests --ignore=tests/test_recursively.py
