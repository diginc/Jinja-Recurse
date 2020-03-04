#!/bin/bash -ex 

pipenv install --dev .

rm -f example/o_file
pipenv run  jinjarecurse -v example/vars.yaml -i example/i_file -o example/o_file

rm -f example/o_dir/*
pipenv run  jinjarecurse -v example/vars.yaml -i example/i_dir -o example/o_dir
