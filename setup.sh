#!/bin/bash

# perform our initialization script
set -x \
   && apt-get update \
   && apt-get upgrade -y \
   && apt-get install -y \
      vim \
      git \
      default-mysql-client \
   && pip3 install -r requirements.txt \
   && set +x

# EOF
