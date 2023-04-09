#!/bin/bash

echo "Hello"

if command -v git >/dev/null 2>&1 ; then
echo "Input accion for repository 1 = clone, 2 = update"
read num
    case $num in 
    1) 
        echo "Input for repository" 
        read repo
        git clone $repo
        ;;
    2)
        pwd
        echo "Directory entry to update repository, example: Repositori/"
        read paht
        cd $paht
        git pull
        ;;
    *)
        echo "Input numbre accion"
    esac
else 
    echo "Git not install"
fi
