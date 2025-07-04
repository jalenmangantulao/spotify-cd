#!/bin/bash

echo "Checking if a compatible Python version is installed..."
python_ver=$(python3 --version)
case "$python_ver" in
    "Python 3.10."*|"Python 3.13."*)
        echo "Compatible Python version found - ("$python_ver")"
        ;;
    *)
        echo "No compatible Python version found."
        ;;
esac

requirements_pckgs=$(grep -oE '(\w+[^\=])+(\d?)' requirements.txt)
user_pip_pckgs=$(pip list | grep -E "(\w.+)(\d+)")

echo "$requirements_pckgs"
