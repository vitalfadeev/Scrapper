#!/bin/sh
grep -i $1 section_combinations.json | tr -d '= '   | sort  -u 