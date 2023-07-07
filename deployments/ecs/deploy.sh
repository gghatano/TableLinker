#! /bin/bash
set -ex

cd `dirname $0`

source set_envs.sh
sh ./build.sh

echo $GIT_SHA
echo $ECR_REPO_NGINX_TAG
echo $ECR_REPO_APP_TAG

ecspresso deploy --config config/rc.yml --update-service

echo deployed
echo $GIT_SHA
echo $ECR_REPO_NGINX_TAG
echo $ECR_REPO_APP_TAG