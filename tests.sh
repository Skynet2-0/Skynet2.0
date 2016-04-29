#currentdir=$(pwd)
currentdir=.
if [ -z $PYTHONPATH ]; then
  PYTHONPATH=$currentdir:..
else
  PYTHONPATH=$currentdir:..:$PYTHONPATH
fi

testdir=tests
topdir=$currentdir

# Echo the PYTHONPATH and testdir for debugging the path.
echo "PYTHONPATH = $PYTHONPATH"
echo "test directory = $testdir"
echo "Top directory = $topdir"

#python3 -m "src.main.tests" #PYTHONPATH="$PYTHONPATH"
#python3 "src/main/tests/WalletTest.py" #PYTHONPATH="$PYTHONPATH"
#python3 "src/main/tests/BogusFormBuilderTest.py" #PYTHONPATH="$PYTHONPATH"

# Official python naming.
python3 -m unittest discover -s $testdir -p '*_test.py' -t $topdir

# Java style test names.
python3 -m unittest discover -s $testdir -p '*Test.py' -t $topdir
