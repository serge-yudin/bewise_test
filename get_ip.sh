#!/bin/bash

echo `ip addr | grep 'inet ' | cut -f6 -d ' ' | cut -f1 -d '/' | awk '!/^172|127/'`
