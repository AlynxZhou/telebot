#!/bin/bash

pip3 freeze > requirements.txt

git add .

git commit -m "A commit."

git push -u origin master
