#Flint [![Build Status](https://travis-ci.org/jdibiccari/flint.svg?branch=master)](https://travis-ci.org/jdibiccari/flint)

Quick Start
------------
    * clone this repository
    * cd flint/
    * create and activate a virtualenv
    * pip install --editable .
    * enter flint --help for usage options


Running Tests
------------
	* install with test dependencies: pip install --editable .[test]
	* py.test [--cov flint]


To-Do
------------
- [ ] logging
- [ ] packaging for distribution (package database files)
- [ ] better test organization


Design Decisions
------------------
1. Language choice: Python
	* I work with python every day in a web app context but have never built a command line tool with it
2. Command line tool package: Click
	* Argument and option parsing
	* Defaults and arg type enforcement
	* Generates help text
	* Nest commands and pass context
	* Some testing support
3. Database vs in-memory storage:
	* Sqlite --> file-based db, standard lib module for db interaction
	* Take advantage of database col types and unique constraints to prevent some errors, validate
4. Retrospective:
	* Click documentation was a little lacking/disjointed for complex examples
	* If I were to make it again I think it would be fun to use python standard lib modules for as much as possible
	* Replacing Click with cmd and argparse? Create an interactive shell/repl vs a command line tool a la git?
	* Spent too much time thinking about packaging aspect at start instead of prototyping and testing
