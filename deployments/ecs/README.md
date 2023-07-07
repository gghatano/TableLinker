# デプロイ環境の構築

## Install Ecspresso
デプロイに [Ecspresso](https://github.com/kayac/ecspresso)を使用します。
```
brew install kayac/tap/ecspresso
```

## デプロイ作業(初回)
`deployments/ecs`ディレクトリに移動して、以下のコマンドを実行すると、デプロイができます。

## 環境変数の設定
direnvなどで以下の環境変数を設定していください。
```
export AWS_REGION=ap-northeast-1
export AWS_PROFILE=tablelinker-deployer
```

## ビルド
コンテナをビルドして、リポジトリにイメージをプッシュします。
```
./build.sh







```

## サービスの作成
※初回のみ必要な作業です。全員で行う必要はありません。
ECS上にサービスを作成しデプロイします。

```
./create.sh
```

# デプロイ作業(2回目以降)
`deployments/ecs`ディレクトリに移動して、以下のコマンドを実行すると、デプロイができます。

## ビルド
コンテナをビルドして、リポジトリにイメージをプッシュします。
```
./build.sh
```

## デプロイ
ECS上にサービスをデプロしします。
```
./deploy.sh
```

# Tips

# クラスターの確認
AWSコンソールより確認できます。
https://ap-northeast-1.console.aws.amazon.com/ecs/home?region=ap-northeast-1

# ログの確認
AWSコンソールのECS>サービス>タスク>コンテナと辿っていくとCloudWatchLogsへのリンクがあります。
CloudWatchLogs上でログが確認可能です。

