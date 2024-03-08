# TableLinker 実行手順

最終更新日 2022-09-16

## はじめに

TableLinker は複数のサービスで構成されているため、
Docker 環境で実行することを推奨します。

Ubuntu 20, MacOS での動作を確認しています。

## コードを取得

GitHub からコード一式を取得します。

以下、ユーザディレクトリの下の github/TableLinker/ ディレクトリに
設定することを前提としてコマンド例を記載していますので、
必要に応じて変更してください。

```
$ mkdir ~/github
$ cd ~/github
$ git clone git@github.com:KMCS-NII/TableLinker.git
$ cd ~/TableLinker/
```

## Docker イメージの作成

api サービスでは、 Python パッケージの依存関係を管理する
[Poetry](https://python-poetry.org/) を利用しています。

CPU アーキテクチャによって利用できるパッケージのバージョンが
異なるため、Docker を動かしているサーバの CPU に応じて
適切な設定ファイルを `api/poetry.lock` にコピーしてください。

このファイルが存在しない場合、イメージを作成する際に
Poetry が依存関係を計算しなおすため、長い時間がかかります。

- Intel x86_64 系の場合

        cp api/poetry.lock-x64 api/poetry.lock

- Arm ARM64 系の場合

        cp api/poetry.lock-aarm64 api/poetry.lock

- 上記以外、または依存関係を計算しなおしたい場合

        rm -f api/poetry.lock

その後、`docker compose build` コマンドを実行します。

```
$ cd ~/github/TableLinker/
$ docker compose build
```

（Docker コマンドに関する注意事項）

- Ubuntu で Docker server を動かしていて、サーバの設定によって
  root 権限が必要な場合は `sudo` を付けてください

- Ubuntu で v20.10.13 より古いバージョンを利用している場合、
  `docker compose` の代わりに `docker-compose` を利用してください

## データベースの初期化と初期データのロード

次のコマンドでデータベースの初期化を行ないます。

```
$ docker compose run --rm api sh initdb.sh
```

このコマンド（initdb.sh スクリプト）は、データベースのマイグレーションと
初期データのロード、および辞書やモデルなどの大きなファイルを
ダウンロードしてインストールします。

初期データには、管理者・テスト用アカウントと、
推奨データセットテンプレートが含まれています。

- 管理者のアカウント

    - メールアドレス: `admin@example.com`
    - パスワード: `password`

    この設定は `api/tablelinker/users/fixtures/users.yaml`に記載されています。

- 推奨データセットテンプレート

    これらのテンプレートの内容は
    `api/tablelinker/dataset_templates/fixtures/standard_templates/`
    に記載されています。

- モデルファイル

    住所ジオコーダの辞書ファイルと、 Transformer のモデルファイルが必要です。
    インストール先は docker-compose.yml 内で環境変数 `JAGEOCODER_DB_DIR`
    および `TRANSFORMER_DIR` によって指定しています。

    いずれも `/opt` の下にインストールされます。このディレクトリは
    docker-compose.yml の設定で `./largefiles` にバインドされているので、
    インストールしたファイルはこのディレクトリの下に保存され、
    Docker コンテナを削除しても消えません。

    次回以降、ここにファイルが残っていれば再利用します。

## Docker サービスを起動

TableLinker は大きなメモリを必要とする処理を複数のワーカープロセスで
並列実行するため、リソースを多めに設定する必要があります。

Docker の設定で、以下のリソースを割り当ててください。

- メモリ: 6GB 以上
- Swap: 2GB 以上
- Disk Image Size: 128 GB 以上

設定を変更したら、次のコマンドでサービスを起動します。

```
$ docker compose up -d
```

api, app, task の準備が終わるまで少し（1分間程度）かかります。
準備状況を確認するには以下のコマンドを実行します。

```
$ docker compose logs -f <サービス名>
```

## ログイン

[http://localhost:8080/](http://localhost:8080/) を開いてください。

Docker を動かしているサーバ以外からアクセスする場合は
Docker サーバのホスト名または IP アドレスで指定することもできます。

## 管理画面

ユーザアカウントの設定などは Django 管理画面から行ないます。

管理画面は [http://localhost:18000/admin/](http://localhost:18000/admin/)
を開いてください。

## メール確認画面

ユーザ新規登録など、メールを送信する場合には、SMTPサーバを以下の
環境変数で指定できます。

- `MAIL_HOST` : ホスト名または IP アドレス
- `MAIL_PORT` : ポート番号
- `MAIL_USER` : ユーザ認証が必要な場合のユーザ名
- `MAIL_PASSWORD` : ユーザ認証が必要な場合のパスワード
- `MAIL_USE_TLS` : TLS のオンオフ（0で TLS を利用しない）

docker-compose.yml の設定では Docker コンテナの smtp で起動する
mailcatcher:1025 を利用します。 mailcatcher は実際にはメールを送信せず、
ウェブUI で確認できる開発用ツールです。

ref: https://mailcatcher.me/

Mailcatcher がハンドリングしたメールを確認したい場合、
[http://localhost:18180/](http://localhost:18180/) をブラウザで開いてください。

## バッチアップロード

サンプルの CSV ファイルをアップロードしたい場合、以下のように
batchupload コマンドを利用します。

```
$ docker compose exec api \
  ./tablelinker/manage.py batchupload --script-args /opendata/toc.csv \
  --email admin@example.com
```

docker-compose.yml により、 `~/github/TableLinker/opendata/` が api コンテナの
/opendata にバインドされているため、ここに置いたファイルは
いつでも api サービスから参照できます。

アップロードしたファイルは `--email` で指定したユーザの
アップロードファイルリストに登録されます。

- カタログ横断検索システム連携

カタログ横断検索を利用してバッチアップロード用の CSV ファイルを
作成することができます。

```
$ cd opendata
$ python3 create_toc.py 'q=AED AND 設置 AND 一覧' rf=AED > 01_AED.csv
$ python3 create_toc.py 'q="介護サービス" AND 一覧' rf=介護 > 02_nursing_care_service_offices.csv
$ python3 create_toc.py 'q="医療機関" AND 一覧' rf=医療 > 03_hospitals.csv
$ python3 create_toc.py 'q="文化財" AND 一覧' > 04_cultural_properties.csv
$ python3 create_toc.py 'q="観光施設" AND 一覧' rf=観光 > 05_tourist_facilities.csv
$ python3 create_toc.py 'q=(イベント OR 祭り) AND 一覧' rf=イベント rf=祭り > 06_events.csv
$ python3 create_toc.py 'q="公衆無線LAN" AND 一覧' rf=無線 > 07_public_wlan_access_points.csv
$ python3 create_toc.py 'q="公衆トイレ" AND 一覧' rf=トイレ > 08_public_toilets.csv
$ python3 create_toc.py 'q="消防水利"' > 09_fire_fighting_facilities.csv
$ python3 create_toc.py 'q="指定緊急避難"' > 10_evacuation_sites.csv
$ python3 create_toc.py 'q="地域年齢別人口"' > 11_populations.csv
$ python3 create_toc.py 'q="公共施設" AND 一覧' > 12_public_facilities.csv
$ python3 create_toc.py 'q="子育て施設"' rf=子育て > 13_childcare_facilities.csv
```

作成した CSV を api コンテナ上で読み込み、記載されているデータセットを
一括登録します。

```
$ docker compose exec api bash
/app# ./tablelinker/manage.py batchupload --email admin@example.com \
  --script-args /opendata/01_AED.csv
```

## 開発者向け情報

docs 以下のフォルダを参照してください。

- AWS 環境のセットアップ

  [./deployments/README.md](./deployments/README.md) を参照してください。

- コードを変更した場合の処理

    - api の下を変更した場合

            $ docker compose down
            $ docker compose build api
            $ docker compose up -d

    - api/graphql_schema の下を変更した場合

            $ docker compose down
            $ docker compose build api
            $ docker compose up -d
            $ docker compose exec app yarn codegen
            $ docker compose restart app

        `yarn codegen` を実行すると `app/src/modules/graphql.ts` が
        更新される可能性があります。


以上
