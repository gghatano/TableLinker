
# CKNA APIについて

### 参考資料
以下のURLにAPIについての詳細がある
https://docs.ckan.org/en/2.8/api/#making-an-api-request

## CKANメタデータ

以下の項目がある
- name (string) – the name of the new dataset, must be between 2 and 100 characters long and contain only lowercase alphanumeric characters, - and _, e.g. 'warandpeace'
- title (string) – the title of the dataset (optional, default: same as name)
- private (bool) – If True creates a private dataset
- author (string) – the name of the dataset’s author (optional)
- author_email (string) – the email address of the dataset’s author (optional)
- maintainer (string) – the name of the dataset’s maintainer (optional)
- maintainer_email (string) – the email address of the dataset’s maintainer (optional)
- license_id (license id string) – the id of the dataset’s license, see license_list() for available values (optional)
- notes (string) – a description of the dataset (optional)
- url (string) – a URL for the dataset’s source (optional)
- version (string, no longer than 100 characters) – (optional)
- state (string) – the current state of the dataset, e.g. 'active' or 'deleted', only active datasets show up in search results and other lists of datasets, this parameter will be ignored if you are not authorized to change the state of the dataset (optional, default: 'active')
- type (string) – the type of the dataset (optional), IDatasetForm plugins associate themselves with different dataset types and provide custom - dataset handling behaviour for these types
- resources (list of resource dictionaries) – the dataset’s resources, see resource_create() for the format of resource dictionaries (optional)
- tags (list of tag dictionaries) – the dataset’s tags, see tag_create() for the format of tag dictionaries (optional)
- extras (list of dataset extra dictionaries) – the dataset’s extras (optional), extras are arbitrary (key: value) metadata items that can be - added to datasets, each extra dictionary should have keys 'key' (a string), 'value' (a string)
- relationships_as_object (list of relationship dictionaries) – see package_relationship_create() for the format of relationship dictionaries (optional)
- relationships_as_subject (list of relationship dictionaries) – see package_relationship_create() for the format of relationship dictionaries (optional)
- groups (list of dictionaries) – the groups to which the dataset belongs (optional), each group dictionary should have one or more of the following keys which identify an existing group: 'id' (the id of the group, string), or 'name' (the name of the group, string), to see which groups exist call group_list()
- owner_org (string) – the id of the dataset’s owning organization, see organization_list() or organization_list_for_user() for available values. This parameter can be made optional if the config option ckan.auth.create_unowned_dataset is set to True.


### リソース
- package_id (string) – id of package that the resource should be added to.
- url (string) – url of resource
- revision_id (string) – (optional)
- description (string) – (optional)
- format (string) – (optional)
- hash (string) – (optional)
- name (string) – (optional)
- resource_type (string) – (optional)
- mimetype (string) – (optional)
- mimetype_inner (string) – (optional)
- cache_url (string) – (optional)
- size (int) – (optional)
- created (iso date string) – (optional)
- last_modified (iso date string) – (optional)
- cache_last_updated (iso date string) – (optional)
- upload (FieldStorage (optional) needs multipart/form-data) – (optional)

## CKAN API

## サイト
サイトのステータスを返します
```
http://demo.ckan.org/api/3/action/site_read
```

## グループ

### グループリスト
http://demo.ckan.org/api/3/action/group_list


## パッケージ
Datasetのこと

### パッケージリスト
```
http://demo.ckan.org/api/3/action/package_list
```

- limit
- offset

### パッケージ検索
```
http://demo.ckan.org/api/3/action/package_search?q=spending
```

先頭の10行を表示
```
http://demo.ckan.org/api/3/action/package_search?q=spending&rows=10
```

### パッケージ表示
```
http://demo.ckan.org/api/3/action/package_show
```
- id 
- use_default_schema
- include_tracking

### パッケージの作成・更新

```
Post http://demo.ckan.org/api/3/action/package_create
Post? http://demo.ckan.org/api/3/action/package_update
```

必須項目
- name
- owner_org(organizatin)


### リソース
Dataset配下のファイルのこと

### リソースの。。
```
http://demo.ckan.org/api/3/action/resource_show
```

- id 
- include_tracking


### リソースの作成

```
Post http://demo.ckan.org/api/3/action/package_create
Post http://demo.ckan.org/api/3/action/package_update
```

項目
- package_id (string) – id of package that the resource should be added to.
- url (string) – url of resource
- revision_id (string) – (optional)
- description (string) – (optional)
- format (string) – (optional)
- hash (string) – (optional)
- name (string) – (optional)
- resource_type (string) – (optional)
- mimetype (string) – (optional)
- mimetype_inner (string) – (optional)
- cache_url (string) – (optional)
- size (int) – (optional)
- created (iso date string) – (optional)
- last_modified (iso date string) – (optional)
- cache_last_updated (iso date string) – (optional)
- upload (FieldStorage (optional) needs multipart/form-data) – (optional)