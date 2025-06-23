# CONTRIBUTING

## Containing environment must use virtualenv <= 20.21.1

Since virtualenv 20.22, python 2.x and <=3.6 has not been supported. In order to support these, use virtualenv <= 20.21.1.

I set this up with:

    $ virtualenv toxrunner
    $ source toxrunner/bin/activate
    (toxrunner)$ pip install -r toxrunner_requirements.txt

and run, e.g.:

    (toxrunner)$ tox -e py27

If you attempt to run eg 2.7 from a newer/standard environment (ie virtualenv >= 20.22), tox will print (somewhat misleading):

    $ tox -e py27
    py27: skipped because could not find python interpreter with spec(s): py27


## Testing

### Setting up deps with apt

    sudo apt update
    sudo apt install -y \
    make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
    libffi-dev liblzma-dev

### Installing interpreters with pyenv

    export PYTHON_CONFIGURE_OPTS="--enable-shared"
    pyenv install -f 2.7
    pyenv install -f 3.6
    pyenv install -f 3.7
    pyenv install -f 3.8
    pyenv install -f 3.9
    pyenv install -f 3.10
    pyenv install -f 3.11
    pyenv install -f 3.12
    pyenv install -f 3.13

I think its important to set PYTHON_CONFIGURE_OPTS, otherwise when virtualenv tries to execute one of the interpreters, they may abort because they cant find .so files. However, I think it did work at some point even when I believe I installed them without this option.


### Running tests

With tox, just do:

    tox

To run tests for only Python 3.7:

    tox -e py37

To pass arguments on to pytest, insert -- separator, and then those arguments. E.g. to look for tests only in folder `tests_unittest` and run only tests matching `da`:

    tox -e py37 -- tests_unittest -k da


#### Running unittests with pytest

Apparently pytest is compatible with tests written entirely in unittest, and it worked out of the box with all tests that were in dbf repo. 


#### pytest command

The command used for auto discovery and execution is simply `pytest`. Because tox 4.x likes it better, its written as 

    python -m pytest


