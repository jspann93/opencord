#!/bin/bash

# if  [["$(uname)" == "cygwin"]]; then
# {
#     powershell.exe -Command "pip install -r requirements.txt"
# } || {
#     powershell.exe -Command "pip3 install -r requirements.txt"
# } || {
#     echo "Error unable to install requirements."
# }
# elif [["$(uname)" == "msys"]]; then
# {
#     powershell.exe -Command "pip install -r requirements.txt"
# } || {
#     powershell.exe -Command "pip3 install -r requirements.txt"
# } || {
#     echo "Error unable to install requirements."
# }
# else
#     echo "Error: Unknown operating system."
#     echo $(uname)
# fi


{
    "pip install -r requirements.txt"
} ||{
    "pip3 install -r requirements.txt"
}||{

    echo "Error unable to install requirements."
}