#!/bin/bash

echo "Attempt to accept new icons but not disrupt our stuff"

git fetch upstream
git checkout master
git merge upstream/master
git merge upstream/master
