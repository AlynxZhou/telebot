#!/bin/bash

echo "{}" > assets/rule.json

git add .

git commit -m "A commit."

git push -u origin master
