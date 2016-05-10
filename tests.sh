#!/usr/bin/env sh

#currentdir=$(pwd)
currentdir=.
if [ -z $PYTHONPATH ]; then
  PYTHONPATH=$currentdir
else
  PYTHONPATH=$currentdir:$PYTHONPATH
fi

testdir="$currentdir/tests"
topdir="$currentdir"

# Echo the PYTHONPATH and testdir for debugging the path.
echo "PYTHONPATH = $PYTHONPATH"
echo "test directory = $testdir"
echo "Top directory = $topdir"

#Install test requirements.
pip install -r tests/testrequirements.txt

#python3 -m "src.main.tests" #PYTHONPATH="$PYTHONPATH"
#python3 "src/main/tests/WalletTest.py" #PYTHONPATH="$PYTHONPATH"
#python3 "src/main/tests/BogusFormBuilderTest.py" #PYTHONPATH="$PYTHONPATH"

# Official python naming.
python -m unittest discover -s "$testdir" -p '*_test.py' -t "$topdir"

# Java style test names.
python -m unittest discover -s "$testdir" -p '*Test.py' -t "$topdir"
