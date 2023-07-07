#! /bin/bash
set -ex

cd `dirname $0`

source set_envs.sh

cd ../..



export GIT_SHA=`git rev-parse HEAD`
export ECR_REPO_NGINX_TAG="$ECR_REPO_NGINX_URL:$GIT_SHA"
export ECR_REPO_APP_TAG="$ECR_REPO_APP_URL:$GIT_SHA"

# ECR Repo Login
aws ecr get-login-password --profile=$AWS_PROFILE --region=$AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO_NGINX_URL
aws ecr get-login-password --profile=$AWS_PROFILE --region=$AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO_APP_URL

# BUILD
docker build -t $ECR_REPO_NGINX_TAG -f containers/nginx/Dockerfile .
docker build -t $ECR_REPO_APP_TAG -f containers/prod/Dockerfile .

# PUSH
docker push $ECR_REPO_NGINX_TAG
docker push $ECR_REPO_APP_TAG

# -----
# 古い処理
# aws ecr get-login-password --profile=$AWS_PROFILE --region=$AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO_NGINX_URL
# aws ecr get-login-password --profile=$AWS_PROFILE --region=$AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO_APP_URL

# # BUILD
# docker-compose -f docker-compose.build.yml build

# # TAG
# docker tag tablelinker_nginx $ECR_REPO_NGINX_URL
# docker tag tablelinker_app $ECR_REPO_APP_URL

# # PUSH
# docker push $ECR_REPO_NGINX_URL
# docker push $ECR_REPO_APP_URL

# export ECR_REPO_NGINX_TAG="$ECR_REPO_NGINX_URL"
# export ECR_REPO_APP_TAG="$ECR_REPO_APP_URL"