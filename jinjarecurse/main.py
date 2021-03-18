""" jinjarecurse (CLI)

Usage:
    jinjarecurse --vars=VARS_FILE --input=INPUT_PATH --output=OUTPUT_PATH

Options:
    -v <file>, --vars   <file>
    -i <file>, --input  <file>
    -o <file>, --output <file>
"""
import jinja2
import yaml
import sys

from pathlib import Path
from docopt import docopt


def main():
    arguments = docopt(__doc__, version='jinjarecurse 0.0.2')
    paths = {
        'variables': Path(arguments['--vars']),
        'input': Path(arguments['--input']),
        'output': Path(arguments['--output']),
    }
    check_paths(**paths)
    variables = read_vars(paths['variables'])
    template(paths, variables)


def template(paths, variables):
    ''' Handles figuring out src/dest file pathing and invoking template writer '''
    if paths['input'].is_dir():
        for search in paths['input'].rglob('*'):
            output = Path(str(search).replace(str(paths['input']), str(paths['output']), 1))
            if search.is_dir():
                print(f"Creating directory: {output}")
                output.mkdir(parents=True, exist_ok=True)
            if search.is_file():
                write_template(search, output, variables)
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
