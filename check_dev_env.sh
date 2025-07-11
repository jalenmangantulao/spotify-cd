#!/bin/bash

echo -e "\e[35mChecking if a compatible Python version is installed..."
python_ver=$(python3 --version)
compatible_pyver="Python 3.10.X | Python 3.13.X"
case "$python_ver" in
    "Python 3.10."*|"Python 3.13."*)
        echo -e "\e[32m\u2714\e[0m Compatible Python version found - ("$python_ver")"
        ;;
    *)
        echo -e "\u274c\ No compatible Python version found. Please install a compatible Python version - ("$compatible_pyver")"
        exit 1
        ;;
esac

echo -e "\e[35mChecking if current user has required Python packages installed...\e[39m"
requirements_pckgs=$(cut -d"=" -f1,3 --output-delimiter=" " requirements.txt > proj_temp.txt)
user_pip_pckgs=$(pip list | tail -n +3 | tr -s " " > user_temp.txt)

awk '
  NR==FNR {
    key = tolower($1) " " $2
    seen[key] = 1
    next
  }
  {
    key = tolower($1) " " $2
    if (!(key in seen)) {
      print "❌ Missing:", $0
      missing_count = 1
    }
  }
  END { 
    if (!missing_count)
        print "✅ All packages from requirements.txt are found in user installed Python packages"
    else
        printf "\nDo you want to install the missing Python packages? [Y/n] "
        getline pkgresp < "/dev/stdin"
        if (index(tolower($0), tolower(pkgresp)) == "y")
            print "Installing missing (missing_count) packages from requirements.txt"
            system("pip install -r requirements.txt")
  }
' user_temp.txt proj_temp.txt
rm user_temp.txt && rm proj_temp.txt
