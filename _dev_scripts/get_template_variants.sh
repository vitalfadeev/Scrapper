#!/bin/sh
grep -i "{{$1" section_templates.json | tr -d ' '   | sort  -u 