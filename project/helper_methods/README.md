If you need helper methods to process data inside views.py, create a new
.py file in this directory and define your methods in them.

Inside views.py, do an `import name_of_file.py` and then call your methods as
`name_of_file.name_of_method()`.

This will keep the views.py file shorter and easier to read while not having to
worry about method name clashes.