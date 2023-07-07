

# セットアップ

## 初回のみ必要な作業
※初回のみ必要な作業です。全員で行う必要はありません。

### Terraform用のアカウントを作成

tablelinker-terraformという名前で、以下の権限を持つTerraform用のアカウントを作成してください。
- AdministratorAccess権限

権限適時調整しても大丈夫です。

### State保存用のS3の作成
terraformは、複数人での使用想定して、s3上にstateを保存します。
`tablelinker-terraform-state`という名前でプライベートのS3作成してください。


## Terraformのインストールする
以下のサイトを参考にインストールをしてください。
https://learn.hashicorp.com/terraform/getting-started/install.html

MacOSの場合、HomeBrewでのインストールが簡単です。
```
brew install terraform
```

## AWS Cliのインストール
AWS Cliのインストールをしてください。
https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-chap-install.html

MacOSの場合、HomeBrewでのインストールが簡単です。
```
brew install awscli
```

## AWSプロフィールの作成
`~/.aws/credentials`を編集してプロフィールを作成する

```
[tablelinker]
aws_access_key_id=XXX
aws_secret_access_key=XXX
```

### AWSのプロフィールを切り替える
環境変数に設定することで可能です。direnvなどで設定すると便利です。
```
export AWS_PROFILE=tablelinker
```

### AWSのプロフィールを確認する
awsのコマンドで確認することができます、
```
aws configure list
```

## Terrafrom 初期化
terraformの初期化を行います。
初めてterraformを実行する場合は、各開発者の環境で実施する必要があります。

```
terraform init
```

## Terrafrom 実行計画の表示
実行計画を表示します。セットアップが問題なければ実行計画が、表示されます。
```
terraform plan
```

## Terrafrom実行
terraformを実行して、AWSに環境を構築します。
```
terraform apply
```

## terraform deployer プロフィールの作成
以下のコマンドで表示された情報を元にプロフィールを作成します。
```
terraform show -json | jq '.values["outputs"].iam_user_deployer.value | {aws_access_key_id: .key_id, aws_secret_access_key: .secret}'
```

`~/.aws/credentials`を編集します。
```
[tablelinker-deployer]
aws_access_key_id=XXX
aws_secret_access_key=XXX
```