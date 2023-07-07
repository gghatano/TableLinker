
export APP_NAME=$(aws ssm get-parameter --name "/tablelinker-rc/app_name" --with-decryption --query "Parameter.Value" --output text)
export APP_DOMAIN=$(aws ssm get-parameter --name "/tablelinker-rc/app_domain" --with-decryption --query "Parameter.Value" --output text)
export ECR_REPO_NGINX_URL=$(aws ssm get-parameter --name "/tablelinker-rc/systems/ecr_nginx_url" --with-decryption --query "Parameter.Value" --output text)
export ECR_REPO_APP_URL=$(aws ssm get-parameter --name "/tablelinker-rc/systems/ecr_app_url" --with-decryption --query "Parameter.Value" --output text)
export AWS_ECS_CLUSTER=$(aws ssm get-parameter --name "/tablelinker-rc/systems/ecr_cluster_name" --with-decryption --query "Parameter.Value" --output text)
export AWS_TARGET_GROUP_ARN=$(aws ssm get-parameter --name "/tablelinker-rc/systems/target_group_arn" --with-decryption --query "Parameter.Value" --output text)
export AWS_SECURITY_GROUP_ID=$(aws ssm get-parameter --name "/tablelinker-rc/systems/sequrity_group_id" --with-decryption --query "Parameter.Value" --output text)
export AWS_SUBNET_IDS_0=$(aws ssm get-parameter --name "/tablelinker-rc/systems/subnet_ids_0" --with-decryption --query "Parameter.Value" --output text)
export AWS_SUBNET_IDS_1=$(aws ssm get-parameter --name "/tablelinker-rc/systems/subnet_ids_1" --with-decryption --query "Parameter.Value" --output text)
export AWS_SSM_PARAMS_PREFIX=$(aws ssm get-parameter --name "/tablelinker-rc/systems/ssm_parameter_arn_prefix" --with-decryption --query "Parameter.Value" --output text)
export AWS_ECS_EXECUTE_ROLE_ARN=$(aws ssm get-parameter --name "/tablelinker-rc/systems/ecs_execute_task_role_arn" --with-decryption --query "Parameter.Value" --output text)
export AWS_ECS_TASK_ROLE_ARN=$(aws ssm get-parameter --name "/tablelinker-rc/systems/ecs_task_role_arn" --with-decryption --query "Parameter.Value" --output text)

export GITHUB_SHA=`git rev-parse HEAD`
export ECR_REPO_NGINX_TAG="$ECR_REPO_NGINX_URL:$GITHUB_SHA"
export ECR_REPO_APP_TAG="$ECR_REPO_APP_URL:$GITHUB_SHA"
