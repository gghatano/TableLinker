# フィルター機能について
TableLinkerには、開発が独自に変換処理を組み込める機能があります。
この組み込み変換処理（フィルター）の実装には、`api/tablelinker/convertors`パッケージにあるAPIを利用する必要があります。

### パッケージの説明

#### `api/tablelinker/customs/<any_name>`
開発者が開発したフィルターを格納するパッケージです。
customs以下にあるパッケージが、Webサーバ起動時に自動的に読み込まれます。


#### `api/tablelinker/convertors/core`
コンバーターを呼び出すための実装があるディレクトリです。
ここにあるAPIを利用して、フィルターを実装します。


#### `api/tablelinker/convertors/celery`
Web側から非同期にフィルターを実行する為のパッケージです。


# フィルターの実装
フィルターを実装する場合、`api/tablelinker/customs`ディレクトリに格納してください。

### 実装例
この例では、特定のカラムを指定の文字数に切り詰める処理をしています。
```
from convertors.core import filters, params, validators

class TruncateFilter(filters.Filter):

    class Meta:
        key = "truncate"
        name = "トランケート"
        params = params.ParamSet(
            params.AttributeParam("attr", label="対象カラム", required=True),
            params.IntParam("length", label="長さ", required=True, validators=(validators.RangeValidator(min=1, max=100),),),
            params.StringParam("omission", label="省略文字", default_value="…"),
        )

    def process_header(self, header, context):
        context.output(header)

    def process_record(self, record, context):
        attr = context.get_param("attr")
        length = context.get_param("length")
        omission = context.get_param("omission")
        value = record[attr]
        record[attr] = value[:length] + (omission if value[length:] else "")
        context.output(record)
```

### 実装方法
Filterは、`filters.Filter`を継承し、Metaクラスを定義する必要があります。

#### 1.Metaの定義
Metaデータ“には、最低限`key`, `name`の定義が必要です。
ユーザに入力させたい場合は、`params`を指定してください。

```
class Meta: 
    key = 'this_is_identity_key'
    name = "列結合"

    description = """
    指定した列を結合した列を新しくするフィルターです。
    """

    help_text = """
    指定した列を結合した列を新しく生成します。
    結合した列は、最後に追加されます。
    """

    params = params.ParamSet(
        params.AttributeParam("attr", label="対象カラム", required=True),
        params.IntParam("length", label="数値のパラメータ", required=True, validators=(validators.RangeValidator(min=1, max=100),),),
        params.StringParam("omission", label="文字のパラメーター", default_value="…"),
    )
```

##### key(必須)
`key`は、Webサーバが、フィルターを特定する為に使われます。その為、システム全体でユニークである必要があります。

##### name(必須)
フィルターの日本語名です。

##### description
フィルターの概要や説明を記載します。

##### help_text
フィルターの使用方法やヘルプを記載します。

##### params
ユーザに指定させたいパラメーターを定義します。
例えば、特定のカラムにフィルターを適用させたい場合は、AttributeParamを定義する必要があります。

ここで指定するパラメーターには、現状以下のものがあります。
- StringParam(文字列)
- IntParam(整数列)
- CollectionParam(他のデータセット)
- AttributeParam(属性)

パラメーターは、Web側の実装が伴うため、開発者が実装することは、できません。


### 2.変換処理の実装
変換処理には、いくつかの実装方法があります。

### `process_xxxxx`を継承する（推奨）
process_xxxxxは、変換処理を簡単に行うために実装された、簡易メソッドです。
これらをオーバライドすることで、処理の実装が可能です。

```
def initial:
    pass

def process_header(self, header, context):
    context.output(header)

def process_record(self, record, context):    
    context.output(record)
```

#### initial
初期化処理を定義するメソッドです。
データセット全体を走査する必要がある場合は、ここで処理をする必要があります。

#### process_header
ヘッダの書き換えを行います。
新しくカラムを追加する場合は、新しいヘッダを追加して書き出します。

```
def process_header(self, header, context):
    header = header + ['new_header']
    context.output(header)
```

#### process_record
データ行の変換処理を行います。
新しくカラムを追加する場合は、新しいデータを追加して書き出します。

```
def process_record(self, record, context):
    record = record + ['new_data']
    context.output(record)
```

### `process`を継承する
`process_xxxx`は、`process`メソッドにより呼び出されています。
変換処理は、`process`メソッドをオーバライドすることでも実装可能です。
詳しくは、[Filter](https://github.com/KMCS-NII/TableLinker/blob/45e2c241f28989e856472a9a305bea24361cf8cc/api/tablelinker/convertors/core/filters.py#L5)の実装をご覧ください。

```
def process(self, context):
    self.initial_context(context)
    self.initial(context)
    type(context)
    context.reset()

    self.process_header(context.next(), context)
    for record in context.read():
        if not self.check_process_record(record, context):
            continue
        self.process_record(record, context)
```

### Filterの登録
実装したフィルターは、システムへの登録が必要です。
登録は、`registry_filter`によって行われます。

```
from convertors.core import filters

filters.registry_filter(<フィルターのクラス>)
```
[実装例](https://github.com/KMCS-NII/TableLinker/blob/develop/api/tablelinker/customs/basics/__init__.py)の実装をご覧ください。

### ContextのAPI
`process_xxx`などで実装する場合、入力・出力は、引数で受け取るcontextに対して、処理を行います。

ここでは、contextのメソッドの紹介をします。実装は、[ここ](https://github.com/KMCS-NII/TableLinker/blob/develop/api/tablelinker/convertors/core/core.py)にあります。

#### output
配列を受け取って、データを書き出します。
```
context.output(['col1', 'col2', 'col3'])
```

#### input
カーソルがある行を読み込みます。
nextなどでカーソルを動かさない限り、何度読んでも同じデータが返ります。
```
context.input()
```

#### read
データセットを読み込んで、for文などで処理する場合に使用します。
```
for record in context.read():
    # process record
```

#### next
readなどを使わずにカーソルを進めます。
```
context.next() # skip header
```

#### reset
カーソルを先頭に戻します。
`seek(0)`に似た処理です。


#### set_data, get_data
initialで作成したデータをprocess_recordなどで使用する場合に、データを格納する場所です。
get_dataで取得することができます。

```
def inital(self, context):
    context.set_data("data_name", "data_value")

def process_recoed(self, record, context):
    data_name = context.get_data("data_name")

```

#### get_param
paramsで定義したデータにアクセスします。
```
 class Meta:
        ...
        params = params.ParamSet(
            params.StringParam("param_name", label="文字", default_value="東京"),
        )

def process_recoed(self, record, context):
    param_name = context.get_param("param_name")
    # param_name is '東京'
```

### Params
Metaデータにparamsを定義することで、ユーザに入力を促すことができます。

#### 基本的な引数

##### name（必須）
パラメーターを特定する為に使うキーです。
フィルター内で、一意である必要があります。

##### description
パラメーターの説明です。

##### help_text
パラメーターのヘルプです。

##### default_value
指定されなかった場合のデフォルト値です。

##### label
パラメーターの日本語名です。

##### validators
ユーザ入力をチェックする為のバリデータのリストです。

##### required
必須チェックです。Web側の画面に必須表示をして、RequiredValidatorを自動登録します。


#### StringParam(文字列)
文字列を受け取るパラメーターです。
独自パラメーターは、ありません。

#### IntParam(整数列)
数値を受け取るパラメーターです。
独自パラメーターは、ありません。

#### AttributeParam(属性)
属性を受け取るパラメーターです。

##### collection_param_name
CollectionParamの結果から属性を指定する場合にCollectionParamのキーを指定します。
このパラメーターが指定されない場合は、変換対象のデータセットの属性をユーザに指定させます。

#### CollectionParam(他のデータセット)
変換対象以外のデータセットを指定させます。

`CollectionProxy`が返ります。

### CollectionProxy
CollectionParamから返るクラスです。
変換対象以外への参照を提供します。

#### idmap(key_index)
対象のデータのIDをキーとしたMapを返します。

引数として`key_index`があり、ここで指定されたキーを元にidmapを生成します。


#### data_read(with_headers=False)
データを読み込みます。

引数として、with_headersを受け取ります。
デフォルト値は、ヘッダを無視します。

```
proxy = ...

for record in proxy.data_read(with_headers=True):
    put record   
```


### Validatorの種類
バリデータは、ユーザが実装できます。

#### RequiredValidator
入力値の必須入力チェックを行います。

#### IntValidator
入力値が整数かをチェックします。

#### FloatValidator
入力値が実数かをチェックします。

#### RangeValidator
入力値を最大と最小で範囲チェックします。

引数として、最大と最小があります。
- max
- min


