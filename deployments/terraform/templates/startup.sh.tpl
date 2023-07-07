#!/bin/bash
# gatewayサーバの初期化スクリプト

sudo apt-get update && \
     apt-get install -y \
     redis-tools \
     redis-server \
     postgresql-client \
     vim \
     unzip \
     jq

# aws cli 2
curl "https://d1vvhvl2y92vvt.cloudfront.net/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

#FILENAME=/home/ubuntu/.envs
#sudo echo export AWS_REGION=${region} >> $${FILENAME}
#sudo echo export APP_NAME=${app_name} >> $${FILENAME}
#SSM_PARAMS=$(aws --region $${AWS_REGION} ssm get-parameters-by-path --path "$${APP_NAME}"  --with-decryption)
#for params in $(echo $${SSM_PARAMS} | jq -r '.Parameters[] | .Name + "=" + .Value'); do
#    sudo echo $${params##*/}
#done > $${FILENAME}
#chmod 600 $${FILENAME}
#chown ubuntu:ubuntu $${FILENAME}
#EOF
