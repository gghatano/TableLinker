"""
カタログ横断検索システムに問い合わせ、
結果に含まれるリソースを toc.csv 形式で出力する。

toc.csv形式：
サイト名,データセット名,リソース名,サイトURL
"""

import csv
import json
from logging import getLogger
from typing import List, Optional
import urllib.parse
import urllib.request

logger = getLogger(__name__)


def usage():
    print("""
Usage: python create_toc.py q=<query> rf=<resource_filter>

Ex.
python create_toc.py 'q=AED AND 設置 AND 一覧' rf=AED > aed.csv
""")


def query_by_xckan(query: str, rows: Optional[int] = None):
    """
    カタログ横断検索システムに問い合わせる

    Parameters
    ----------
    query: str
        横断検索システムに送信する問い合わせ文字列
        例：'AED AND 設置 AND 一覧'

    rows: int
        検索するレコード数
        未指定の場合はデフォルト値 = 1000
    """
    rows = rows or 1000
    api_endpoint = 'https://search.ckan.jp/backend/api/'
    api_method = 'package_search'
    query_url = '{}{}?q={}&rows={}'.format(
        api_endpoint, api_method, urllib.parse.quote(query), rows)
    with urllib.request.urlopen(query_url) as response:
        body = response.read()
        data = json.loads(body)

    return data


def get_resources(
        query: str,
        resource_filters: Optional[List[str]] = None,
        formats: Optional[List[str]] = None):
    """
    query_by_xckan で検索し、その結果を解析してリソース一覧を取得する

    Parameters
    ----------
    query: str
        横断検索システムに送信する問い合わせ文字列
        例：'AED AND 設置 AND 一覧'

    result: dict
        query_by_xckan の返す結果

    resource_filters: List[str] (Optional)
        リソースファイル名に含まれるべき部分文字列のリスト
        複数指定した場合はいずれかが含まれれば取得する
        None の場合は全てのリソースファイルを返す

    formats: List[str] (Optional)
        抽出するファイルフォーマット（拡張子）
    """
    resources = []
    result = query_by_xckan(query)

    if result.get('success', False) is not True:
        return resources

    # with open("result.json", "w") as f:
    #     f.write(json.dumps(result, indent=2, ensure_ascii=False))

    if formats is None:
        formats = ['pdf', 'csv', 'xls', 'xlsx']
    else:
        formats = [x.lower() for x in formats]

    for package in result['result']['results']:
        package_meta = {
            "xckan_id": package['xckan_id'].strip(),  # "www.data.go.jp__data__dataset:mext_20150713_0035",
            "xckan_title": package['xckan_title'].strip(),  # "その他_財政制度等審議会の「財政健全化計画等に関する建議」に対する文部科学省としての考え方",
            "xckan_site_name": package['xckan_site_name'].strip(),  # "DATA GO JP データカタログサイト",
            # "https://www.data.go.jp/data/dataset/mext_20150713_0035",
            "xckan_site_url": package['xckan_site_url'].strip(),
        }
        for resource in package.get('resources', []):
            if ('url' not in resource and 'download_url' not in resource) \
                    or resource['id'] is None:
                continue

            resource_format = resource.get('format') or 'null'
            if resource_format.lower() not in formats:
                msg = "Skip resource {} since its format is {}"
                logger.debug(msg.format(resource['id'], resource_format))
                continue

            url = resource.get('download_url', resource.get('url'))
            name = resource.get('name', None)

            if resource_filters not in (None, []):
                passed = False
                for resource_filter in resource_filters:
                    if resource_filter in name:
                        passed = True
                        break

                if passed is False:
                    msg = "Skip resource {} since name doesn't contain '{}'."
                    logger.debug(msg.format(resource['id'], resource_filters))
                    continue

            if name is None:
                raise RuntimeError("Name is None. {}".format(
                    resource))

            resources.append([
                package_meta["xckan_site_name"],
                package_meta["xckan_title"],
                name.strip(), url])

    return resources


if __name__ == '__main__':
    import logging
    import sys

    logger.setLevel(logging.DEBUG)
    args = sys.argv

    queries = []
    resource_filters = []

    for arg in args[1:]:
        if arg.startswith(('-h', '--help',)):
            usage()
            exit(0)

        if arg[0:2] == 'q=':
            queries.append(arg[2:].strip())
        elif arg[0:3] == 'rf=':
            resource_filters.append(arg[3:].strip())
        else:
            logger.warning("Invalid parameter '{}' (ignored)".format(arg))

    if len(queries) == 0:
        logger.error("Query ('q=xxx') is required.")
        exit(1)

    if len(queries) > 1:
        query = ' OR '.join(['({})'.format(x) for x in queries])
    else:
        query = queries[0]

    resources = get_resources(
        query=query,
        resource_filters=resource_filters)

    if len(resources) == 0:
        logger.warning("No resources")
        exit(0)

    csvwriter = csv.writer(sys.stdout, quoting=csv.QUOTE_ALL)
    csvwriter.writerow(["サイト名", "データセット名", "リソース名", "サイトURL"])

    for resource in resources:
        csvwriter.writerow(resource)
