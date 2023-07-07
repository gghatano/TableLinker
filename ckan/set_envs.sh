export AWS_REGION=ap-northeast-1
export AWS_PROFILE=tablelinker-deployer

export AWS_ECS_EXECUTE_ROLE_ARN=$(aws ssm get-parameter --name "/tablelinker-rc/systems/ecs_execute_task_role_arn" --with-decryption --query "Parameter.Value" --output text)
export AWS_ECS_TASK_ROLE_ARN=$(aws ssm get-parameter --name "/tablelinker-rc/systems/ecs_task_role_arn" --with-decryption --query "Parameter.Value" --output text)

export ECR_REPO_CKAN_CKAN_URL=$(aws ssm get-parameter --name "/tablelinker-rc/systems/ckan/ecr_ckan_ckan_url" --with-decryption --query "Parameter.Value" --output text)
export ECR_REPO_CKAN_PSQL_URL=$(aws ssm get-parameter --name "/tablelinker-rc/systems/ckan/ecr_ckan_psql_url" --with-decryption --query "Parameter.Value" --output text)
export ECR_REPO_CKAN_SOLR_URL=$(aws ssm get-parameter --name "/tablelinker-rc/systems/ckan/ecr_ckan_solr_url" --with-decryption --query "Parameter.Value" --output text)

export AWS_ECS_CLUSTER=$(aws ssm get-parameter --name "/tablelinker-rc/systems/ckan/cluster_name" --with-decryption --query "Parameter.Value" --output text)
export AWS_TARGET_GROUP_ARN=$(aws ssm get-parameter --name "/tablelinker-rc/systems/ckan/target_group_arn" --with-decryption --query "Parameter.Value" --output text)
export AWS_SECURITY_GROUP_ID=$(aws ssm get-parameter --name "/tablelinker-rc/systems/ckan/sequrity_group_id" --with-decryption --query "Parameter.Value" --output text)

export AWS_ALB_URL=$(aws ssm get-parameter --name "/tablelinker-rc/systems/alb_url" --with-decryption --query "Parameter.Value" --output text)

export AWS_SUBNET_IDS_0=$(aws ssm get-parameter --name "/tablelinker-rc/systems/subnet_ids_0" --with-decryption --query "Parameter.Value" --output text)
export AWS_SUBNET_IDS_1=$(aws ssm get-parameter --name "/tablelinker-rc/systems/subnet_ids_1" --with-decryption --query "Parameter.Value" --output text)

export EFS_CKAN_DATA_ID=$(aws ssm get-parameter --name "/tablelinker-rc/systems/ckan/data_id" --with-decryption --query "Parameter.Value" --output text)
export EFS_CKAN_REDIS_DATA_ID=$(aws ssm get-parameter --name "/tablelinker-rc/systems/ckan/redis_data_id" --with-decryption --query "Parameter.Value" --output text)
export EFS_CKAN_SOLR_DATA_ID=$(aws ssm get-parameter --name "/tablelinker-rc/systems/ckan/solr_data_id" --with-decryption --query "Parameter.Value" --output text)
export EFS_CKAN_PSQL_DATA_ID=$(aws ssm get-parameter --name "/tablelinker-rc/systems/ckan/psql_data_id" --with-decryption --query "Parameter.Value" --output text)

export CKAN_SITE_ID=default
export CKAN_SITE_URL=http://${AWS_ALB_URL}:5000
export POSTGRES_PASSWORD=ckan
export POSTGRES_PORT=5432
export DATASTORE_READONLY_PASSWORD=datastore
