#####################################
# TerraForm Variable Settings
#####################################
#AWS Settings
//access_key = ""
//secret_key = ""
region = "ap-northeast-1"

#App Name
app_name = "tablelinker-rc"
app_domain = "xxxxxxx"

vpc_cidr_block = "10.200.0.0/16"
cidr_blocks = [
  "10.200.10.0/24",
  "10.200.11.0/24"
]

# App
app_instance_class = "t2.small"
ckan_instance_class = "t2.small"

# DB
db_instance_class = "db.t2.small"
db_name = "tablelinker"
db_username = "tablelinker"
db_password = "tablelinker"

//cidr_block        = "${lookup(var.subnet_public_a, "${terraform.workspace}", var.subnet_public_a["default"])}"
//variable "subnet_public_a" {
//   default = {
//     default    = "172.30.3.0/24"
//     stg        = "172.30.3.0/24"
//     pro        = "172.30.7.0/24"
//   }
// }