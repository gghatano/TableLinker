#!/bin/sh
set -e

# If we don't already have a config file, bootstrap
if [ ! -e "$CONFIG" ]; then
  ckan make-config --no-interactive ckan "$CONFIG"
fi
ckan db init
echo 'yes' | ckan sysadmin add admin email=test@test.com password=adminadmin

exec "$@"
