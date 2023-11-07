#!/bin/bash

echo "Hello"

if command -v git >/dev/null 2>&1 ; then
    echo "Input action for repository 1 = clone, 2 = pull"
    read num
    case $num in 
        1) 
            echo "Input URL for repository to clone" 
            read repo
            if git clone $repo; then
                echo "Repository cloned successfully"
            else
                echo "Failed to clone repository"
            fi
            ;;
        2)
            echo "Directory entry to update repository, example: Repositori/"
            read path
            if [ -d "$path" ]; then
                cd $path
                if git pull; then
                    echo "Repository updated successfully"
                else
                    echo "Failed to update repository"
                fi
            else
                echo "Directory does not exist"
            fi
            ;;
        *)
            echo "Invalid input. Please enter 1 to clone or 2 to update a repository."
    esac
else 
    echo "Git is not installed. Please install Git to use this script."
fi
