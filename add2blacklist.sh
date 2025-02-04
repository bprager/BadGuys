#!/usr/bin/env sh

if [ $# -eq 0 ]
  then
	  echo "No arguments (ip address) supplied"
	  exit 1
fi

sudo ipset add blacklist $1
