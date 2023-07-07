import csv
import logging
import os
import tracemalloc
import nkf


def get_encode(file, mode="nkf", buffer_size=16384):  # noqa: C901

    guessed = None
    buffer = ""
    if mode == "nkf":
        if isinstance(file, str) or isinstance(file, os.PathLike):
            with open(file, mode="rb") as f:
                buffer = f.read(buffer_size)
                # 0xEF(BOM)
                if len(buffer) > 0 and buffer[0] == 239:
                    guessed = "UTF-8-SIG"

        else:
            with file.open(mode="rb") as f:
                buffer = f.read(buffer_size)
                # 0xEF(BOM)
                if len(buffer) > 0 and buffer[0] == 239:
                    guessed = "UTF-8-SIG"

    elif mode == "nkf_content":
        try:
            buffer = file.read(buffer_size)
            # 0xEF(BOM)
            if len(buffer) > 0 and buffer[0] == 239:
                guessed = "UTF-8-SIG"

        finally:
            if not file.closed:
                file.seek(0)

    if guessed is None:
        guessed = nkf.guess(buffer)
        if guessed == "BINARY":
            guessed = "UTF-8"

    # elif mode == "chardet":
    #     detector = UniversalDetector()
    #     if type(file) is File:
    #         with file.open(mode="rb") as f:
    #             for binary in f:
    #                 detector.feed(binary)
    #                 if detector.done:
    #                     break
    #     else:
    #         with open(file, mode="rb") as f:
    #             for binary in f:
    #                 detector.feed(binary)
    #                 if detector.done:
    #                     break
    #     detector.close()
    #     encoding = detector.result["encoding"]

    #     # if encoding == "SHIFT_JIS":
    #     #     encoding = "CP932"
    #     # elif encoding == "Windows-1254":
    #     #     encoding = "CP932"

    #     return encoding

    return guessed


def gen_csv_reader(file):
    # TODO: 事前に調べる方法があるので対応する
    return csv.reader(file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True,)


def format_bytes(size):
    power = 2 ** 10  # 2**10 = 1024
    n = 0
    power_labels = ["B", "MB", "GB", "TB"]
    while size > power and n <= len(power_labels):
        size /= power
        n += 1
    return "current used memory: {:.3f} {}".format(size, power_labels[n])


def log_memory():
    snapshot = tracemalloc.take_snapshot()
    size = sum([stat.size for stat in snapshot.statistics("filename")])
    return format_bytes(size)


def batch_qs(qs, batch_size=1000):
    """
    Returns a (start, end, total, queryset) tuple for each batch in the given
    queryset.
    Usage:
        # Make sure to order your querset
        article_qs = Article.objects.order_by('id')
        for start, end, total, qs in batch_qs(article_qs):
            print "Now processing %s - %s of %s" % (start + 1, end, total)
            for article in qs:
                print article.body
    """
    total = qs.count()
    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        yield (start, end, total, qs[start:end])


def enable_sql_logging(flag: bool):
    l = logging.getLogger('django.db.backends')
    if flag:
        l.setLevel(logging.DEBUG)
        l.addHandler(logging.StreamHandler())
    else:
        l.setLevel(logging.WARNING)
        l.removeHandler(logging.StreamHandler())
