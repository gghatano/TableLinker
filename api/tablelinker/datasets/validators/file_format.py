from rest_framework import serializers
from shared.utils import get_encode


class FileFormatValidator:
    requires_context = True

    # ALLOW_ENCODINGS = ['UTF-8', 'Shift_JIS', 'EUC-JP']
    ALLOW_ENCODINGS = ["UTF-8", "UTF-8-SIG", "Shift_JIS", "CP932", "ASCII"]

    def __call__(self, value, serializer_field):
        self.valid_min_file_size(value)
        self.valid_max_file_size(value)

        value.file.seek(0)
        content = value.file.read()
        value.file.seek(0)

        encoding = get_encode(value, mode="nkf_content")
        self.valid_encoding(encoding)

        # self.valid_unicode_decode(content, encoding)

        try:
            mode = "surrogateescape"
            # mode = 'strict'
            content = content.decode(encoding, mode)
            self.valid_csv(content)
        except UnicodeDecodeError as e:
            value = e.object[e.start : e.end]
            message = "変換できない文字がありました。"
            raise serializers.ValidationError(message)

    def valid_min_file_size(self, file):
        if file.size < 1:
            message = "ファイルの内容が空です。"
            raise serializers.ValidationError(message)

    def valid_max_file_size(self, file):
        if file.size > 100_000_000:
            message = "CSVファイルサイズが100MBを超えています。"
            raise serializers.ValidationError(message)

    def valid_encoding(self, encoding):
        if encoding == "BINARY":
            message = "CSVファイルでは、ありません。バイナリファイルの可能性があります。"
            raise serializers.ValidationError(message)
        if encoding not in self.ALLOW_ENCODINGS:
            message = "Shift_JIS,UTF-8, UTFBOM付きのみアップロードできます。({})".format(encoding)
            raise serializers.ValidationError(message)

    def valid_csv(self, content):
        if ("html>" in content) or ("<html" in content) or ("!DOCTYPE" in content) or ("head>" in content):
            # if re.search("<(\"[^\"]*\"|'[^']*'|[^'\">])*>", content) is not None:
            message = "HTMLファイルの可能性があります。"
            raise serializers.ValidationError(message)

    def valid_unicode_decode(self, content, encoding):
        try:
            content.decode(encoding)
        except UnicodeDecodeError as e:
            print(e)
            message = "変換できない文字があります。({})".format(encoding)
            raise serializers.ValidationError(message)
