# Jinja Recurse CLI tool

Jinja Recursive Templating for the CLI.  Recursively template one file or many folders of many files like a config management languages allow, without the whole config management language.  Useful if you're switching from managing an application from config management to just docker and need some simple templating logic.

## Example usage

```
# Directory
$ jinjarecurse -v example/vars.yaml -i example/i_dir -o example/o_dir
WARNING: example/o_file (output) exists and any conflicting files will be overwritten
Writing from example/i_file to example/o_file

# Single File
$ jinjarecurse -v example/vars.yaml -i example/i_file -o example/o_file
Writing from example/i_dir/i_file_2 to example/o_dir/i_file_2
Writing from example/i_dir/i_file to example/o_dir/i_file
Writing from example/i_dir/i_file_1 to example/o_dir/i_file_1
```

## Tests

To run the unit tests:
```
# First install the dependencies
$ pipenv install --dev .

# Then invoke pytest
$ pipenv run py.test -vvvs
```
