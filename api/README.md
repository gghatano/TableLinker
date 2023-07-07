# GettingStart

## Docker からの Django の起動

以下のコマンドで起動します。

```
docker-compose up api
```

## マイグレーション

```
./manage.py migrate
```

## 初期データなど

### 標準テンプレート

yaml ファイルは、以下の場所に格納されている
`tablelinker/dataset_templates/fixtures/standard_templates`

ロードコマンド

```
./manage.py loaddata dataset_templates/fixtures/standard_templates
```

### 意味型

yaml ファイルは、以下の場所に格納されている
`tablelinker/datasets/fixtures/attr_type.yaml`

ロードコマンド

```
./manage.py loaddata datasets/fixtures/attr_type.yaml
```
