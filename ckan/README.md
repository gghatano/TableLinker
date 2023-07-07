# 起動方法

## 準備
/etc/hostsに以下の行を追加
```
127.0.0.1 ckan
```

## 初回起動

.envファイルを作成しましす。
```
cp .env.template .env
```

コンテナ伸びるルドをします。
```
docker-compose build
```

初回起動のみDBの初期化に時間がかかり、タイムアウトするので、DBのみ先に起動します。
```
docker-compose up -d db
```

CKANを起動します。
```
docker-compose up ckan
```

ブラウザでアクセスします。
```
open http://ckan:5000
```

CKANの画面が、表示されるれるとセットアップ完了です。

## ２回目以降起動
２回目以降は、以下のコマンドで実行できます
```
docker-compose start ckan
```

# 各種コマンド

## 起動しているCKANコンテナにbashでアクセスする

```
docker-compose run ckan bash
```

## テストデータの生成
```
docker-compose run ckan ckan create-test-data 
```

## システムユーザの追加
```
docker-compose run ckan ckan sysadmin add <username> 
```

コマンドの実行例 
```
docker-compose run ckan ckan sysadmin add admin email=test@test.com password=adminadmin  
```

## install
以下のサイトを参考にする
- https://docs.ckan.org/en/2.8/maintaining/installing/install-from-package.html
- 最初のインストールでnginxだけ単独でインストールしないとコケる。
- 実施してしまった場合は、一旦apacheを消して、nginx -> apacheの順序でインストールすること
- datastoreは、rokeとdbの作成だけよい
- Uploadは、storage_dirを設定しないと出てこない

システムユーザ追加
```
sudo ckan sysadmin add admin email=test@test.com password=adminadmin  
```
