""" Yet Another Jinja (YaJinja) (CLI)

Usage:
    yajinja [-m] --vars=VARS_FILE --input=INPUT_PATH --output=OUTPUT_PATH

Options:
    -v <file>, --vars   <file>
    -i <file>, --input  <file>
    -o <file>, --output <file>
    -e <environment> ...
"""
import jinja2
import yaml
import sys

from pathlib import Path
from docopt import docopt


def main():
    arguments = docopt(__doc__, version='YaJinja 0.1')
    paths = {
        'variables': Path(arguments['--vars']),
        'input': Path(arguments['--input']),
        'output': Path(arguments['--output']),
    }
    check_paths(**paths)
    variables = read_vars(paths['variables'])
    #print(variables)
    template(paths, variables)


def template(paths, variables):
    ''' Handles figuring out src/dest file pathing and invoking template writer '''
    if paths['input'].is_dir():
        for search in paths['input'].rglob('*'):
            if search.is_file():
                output = str(search).replace(str(paths['input']), str(paths['output']))
                write_template(search, Path(output), variables)
    elif paths['input'].is_file():
        write_template(paths['input'], paths['output'], variables)


def write_template(ipath, opath, variables):
    print("Writing from {} to {}".format(ipath, opath))
    template = jinja2.Template(ipath.read_text())
    opath.write_text(template.render(**variables))


def check_paths(**kwargs):
    bail = False
    for k, path in kwargs.items():
        if k == 'variables' and not path.is_file():
            print("ERROR: {} ({}) is not a file".format(path, k), file=sys.stderr)
            bail = True
        if k == 'input' and not path.exists():
            print("ERROR: {} ({}) does not exist".format(path, k), file=sys.stderr)
            bail = True
        if k == 'output' and path.exists():
            print("WARNING: {} ({}) exists and any conflicting files will be overwritten".format(path, k), file=sys.stderr)
    if bail:
        sys.exit(1)


def read_vars(var_file):
    var_obj = Path(var_file)
    return yaml.safe_load(var_obj.read_text())


if __name__ == "__main__":
    main()
