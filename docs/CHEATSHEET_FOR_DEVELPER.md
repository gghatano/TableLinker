
開発者向けのチートシートです。

## Django Commands

### create app
```
./manage.py startapp <app_name>
```

### load fixtures
```
./manage.py loaddata <fixture_name>
```

## Django Tips

### User modelの参照
```
from django.contrib.auth import get_user_model
User = get_user_model()
```

## Poetory

poetoryを採用しています。

### Install poetry
https://poetry.eustace.io/docs/ 
```
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```

### ライブラリの追加
```
poety add <any>
```

## Lints

### Format
```
docker-compose run app black
```

### Lint
```
docker-compose run app flake8
```

### poetry to requirements.lock
```
poetry run pip freeze > requirements.lock
```

# Links
- https://narito.ninja/blog/detail/38/
- https://docs.djangoproject.com/ja/2.0/ref/models/fields/
- [管理画面の設定](https://qiita.com/zenwerk/items/044c149d93db097cdaf8)

