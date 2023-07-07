#! /bin/bash
set -ex

sh ./build.sh

source set_envs.sh

cd `dirname $0`

ecspresso create --config config/rc.yml