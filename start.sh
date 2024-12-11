#!/bin/bash

docker run -it --rm \
	--name mysql-backup \
	-v `pwd`:/opt/git:rw \
	python:3 bash

# EOF

