from collections import OrderedDict
from inspect import (
    cleandoc,
)  # This is used to handle the triple quote string indentation

from jinjarecurse.main import (
    check_paths,
    read_vars,
    template,
    write_template,
)

import pytest


@pytest.fixture()
def variables():
    return OrderedDict(
        {
            "dictionary": {
                "city": "New York",
                "state": "New York",
                "street": "123 North Ave",
            },
            "layer_1": {"layer_2": {"layer_3": "last"}},
            "list": ["ABC", "DEF", "HJK"],
            "number": 1,
            "root": "/",
        }
    )


@pytest.fixture()
def var_file(tmp_path):
    vars = cleandoc(
        """
        #comment: not available
        root: /
        number: 1
        dictionary:
            street: 123 North Ave
            city: New York
            state: New York
        list:
            - ABC
            - DEF
            - HJK
        layer_1:
            layer_2:
                layer_3: last
        """
    )
    path = tmp_path / "vars.yaml"
    path.write_text(vars)

    return path


@pytest.fixture()
def input_file(tmp_path):
    vars = cleandoc(
        """
        # Top level
        {{root}}
        {{number}}
        {{dictionary}}
        {{list}}
        {{layer_1}}

        # Nested data

        {{dictionary.street}}
        {{dictionary.city}}
        {{dictionary.state}}
        {{layer_1.layer_2.layer_3}}
        """
    )
    path = tmp_path / "i_file.txt"
    path.write_text(vars)

    return path


@pytest.fixture()
def output_file(tmp_path):
    path = tmp_path / "o_file.txt"

    return path


def test_read_vars(var_file):
    """Test that read_vars works as expected."""
    output = read_vars(var_file)

    assert output == {
        "dictionary": {
            "city": "New York",
            "state": "New York",
            "street": "123 North Ave",
        },
        "layer_1": {"layer_2": {"layer_3": "last"}},
        "list": ["ABC", "DEF", "HJK"],
        "number": 1,
        "root": "/",
    }


def test_check_paths(var_file, input_file, output_file):
    """Test that check_paths works as expected."""
    check_paths(variables=var_file, input=input_file, output=output_file)


def test_check_paths_error_var_dir(var_file, input_file, output_file, capsys):
    """Test that check_paths raises errors as expected."""
    with pytest.raises(SystemExit):
        check_paths(
            variables=var_file.parent, input=input_file, output=output_file
        )

    assert "(variables) is not a file" in capsys.readouterr().err


def test_check_paths_error_input_nonexistent(
    var_file, input_file, output_file, capsys
):
    """Test that check_paths raises errors as expected."""
    with pytest.raises(SystemExit):
        check_paths(
            variables=var_file,
            input=(input_file.parent / "nonexistent_file.txt"),
            output=output_file,
        )

    assert "(input) does not exist" in capsys.readouterr().err


def test_check_paths_error_output_exists(
    var_file, input_file, output_file, capsys
):
    """Test that check_paths raises errors as expected."""
    output_file.write_text("Some existing output")
    check_paths(variables=var_file, input=input_file, output=output_file)

    assert (
        "(output) exists and any conflicting files will be overwritten"
        in capsys.readouterr().err
    )


def test_write_template(variables, input_file, output_file, capsys):
    """Test that write_template works as expected."""
    write_template(input_file, output_file, variables)

    assert output_file.read_text() == cleandoc(
        """
        # Top level
        /
        1
        {'city': 'New York', 'state': 'New York', 'street': '123 North Ave'}
        ['ABC', 'DEF', 'HJK']
        {'layer_2': {'layer_3': 'last'}}

        # Nested data

        123 North Ave
        New York
        New York
        last
        """
    )


def test_template(variables, input_file, output_file, capsys):
    """Test that template works as expected."""
    paths = {"variables": var_file, "input": input_file, "output": output_file}
    template(paths, variables)

    assert output_file.read_text() == cleandoc(
        """
        # Top level
        /
        1
        {'city': 'New York', 'state': 'New York', 'street': '123 North Ave'}
        ['ABC', 'DEF', 'HJK']
        {'layer_2': {'layer_3': 'last'}}

        # Nested data

        123 North Ave
        New York
        New York
        last
        """
    )
