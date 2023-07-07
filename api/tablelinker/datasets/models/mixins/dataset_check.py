import codecs
import csv
from enum import IntEnum

from django.core.files import File
from django.db import models

from shared.utils import get_encode


class AnalyzeStatus(IntEnum):

    SUCCESS = 0  # 成功
    IGNORE_FORMAT = 1  # CSV形式ではない
    IGNORE_CHARSET = 2  # 未対応の文字コード
    OVER_COLUMNS = 3  # 列数が上限超過
    OVER_SIZE = 4  # ファイルサイズがオーバー
    EMPTY = 5  # 空ファイル
    NOT_EQ_COLUMNS = 6  # 列数が見出し行と一致しない行を含む
    HTML = 7  # Ccat SV形式ではない
    UnicodeDecode = 10
    UNKNOWN = 99  # 不明なエラー


class DatasetCheckMixin(models.Model):
    """
    注釈関連の実装
    """

    class Meta:
        abstract = True

    def check_file(  # noqa: C901
        self,
        original_file=None,
        delimiters=",",
        support_charset=["SHIFT_JIS", "UTF-8", "CP932", "ASCII"],
        limit_file_size=100000000,
        min_file_size=0,
        max_columns=1000,
        codec_mode="strict",
        encode_mode="nkf",
    ):
        if original_file is None:
            file = self.original_file
        else:
            file = File(original_file)

        # check encoding
        encoding = get_encode(file, encode_mode)
        if encoding.upper() not in support_charset:
            self.analyzed_status = AnalyzeStatus.IGNORE_CHARSET
            return self.analyzed_status

        # check EMPTY
        size = file.size
        if size <= min_file_size:
            self.analyzed_status = AnalyzeStatus.EMPTY
            return self.analyzed_status

        # check OVER_SIZE
        if size > limit_file_size:
            self.analyzed_status = AnalyzeStatus.OVER_SIZE
            return self.analyzed_status

        # open file
        try:
            info = codecs.lookup(encoding)
            with info.streamreader(file.open(mode="rb"), codec_mode) as csv_file:

                # check HTML
                html = csv_file.readline().lower()
                if ("html>" in html) or ("<html" in html) or ("!DOCTYPE" in html) or ("head>" in html):
                    self.analyzed_status = AnalyzeStatus.HTML
                    return self.analyzed_status
                csv_file.seek(0)

                # check format
                sample = "\n".join([csv_file.readline() for i in range(20)])
                dialect = csv.Sniffer().sniff(sample, delimiters)

                # refresh
                csv_file.seek(0)

                # read csv
                csv_reader = csv.reader(csv_file, dialect)

                # headers
                header_row = next(csv_reader)

                # check columns nums
                num_of_columns = len(header_row)
                if num_of_columns > max_columns:
                    self.analyzed_status = AnalyzeStatus.OVER_COLUMNS
                    return self.analyzed_status

                # check row columns
                rows = [row for row in csv_reader]
                for rows in rows:
                    num_of_row_cols = len(rows)
                    if num_of_row_cols == 0:
                        continue
                    if num_of_row_cols != num_of_columns:
                        self.analyzed_status = AnalyzeStatus.NOT_EQ_COLUMNS
                        return self.analyzed_status

        except csv.Error:
            self.analyzed_status = AnalyzeStatus.IGNORE_FORMAT
            return self.analyzed_status
        except UnicodeDecodeError:
            self.analyzed_status = AnalyzeStatus.UnicodeDecode
            return self.analyzed_status

        # SUCCESS
        self.analyzed_status = AnalyzeStatus.SUCCESS
        return self.analyzed_status
