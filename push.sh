#!/bin/bash

git add .

if [[ -n "${*}" ]]; then
    git commit -m "${*}"
else
    git commit -m "A commit."
fi

git push -u origin master

