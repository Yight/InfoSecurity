#!/bin/bash
# runcelecry.sh

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

python manage.py celeryd -v 2 -B -s celery -E -l INFO
