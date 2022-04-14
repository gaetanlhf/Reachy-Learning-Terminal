#!/bin/bash

LINES=$(find . -name '*.py' -print0 | xargs -0 cat | wc -l)
echo "There are $LINES lines of Python code in the src directory"