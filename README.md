Common Keys
===========

This is meant to be a tool that captures input to an X11 environment (no command-line only, sorry) in order to help the user spot commonly-typed patterns that they might do well to add expansions for in some cool text-expansion program (or whatever they're called).

Setup
-----

because `pyvenv-3.3` is annoying:<br/>
1. make the venv. `pyvenv-3.3 common-keys` (or whatever you want to call it)
1. `cd common-keys`
1. `source bin/activate` (assuming you’re using bash)
1. `git init`
1. `git remote add origin <github clone URL>`
1. `git fetch`
1. `git checkout --track origin/master`
1. put `get-pip.py` in the directory
1. `python get-pip.py`
1. `pip install -r requirements.txt`
1. ???
1. PROFIT
