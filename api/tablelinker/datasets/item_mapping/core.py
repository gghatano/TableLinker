import json

from django.conf import settings

from .mapping import ItemsPair, similarity


class ItemMappingResult(object):
    def __init__(self, source_index, title=None, message=None, filter_key=None, filter_params=None):
        """
    コンストラクタ
    :param message: メッセージ
    :param filter_key: フィルターキー
    :param filter_params: フィルターパラメータ
    """
        self.message = message
        self.source_index = source_index
        self.filter_key = filter_key
        self.filter_params = filter_params


def item_mapping(dataset, target):
    """
    This function is used to map items to their respective categories.
    :param item: item to be mapped
    :return: category of the item
    """
    suggests = []

    suggests.extend(item_mapping_rename(dataset, target))  # カラムの名前の変更
    suggests.extend(item_mapping_insert(dataset, target))  # カラムの追加
    suggests.extend(item_mapping_position(dataset, target))  # カラムの位置情報の変更

    return suggests


def item_mapping_rename(dataset, target_dataset):
    """
  カラムの位置情報に関するマッピング
  """
    dataset_attr_names = dataset.attr_names
    target_attr_names = target_dataset.attr_names

    suggests = []
    pair = ItemsPair(
        dataset_attr_names, target_attr_names,
        similarity=similarity)
    for result in pair.mapping():
        # attrをtarget_attrの位置に移動する
        attr_index = result[0]  # targetのカラム(移動対象)
        attr_name = result[1]  # targetのカラム(移動対象)
        target_attr_index = result[2]  # target_datasetのカラム(移動先)
        target_attr_name = result[3]  # target_datasetのカラム(移動先)
        # sim = result[4]  # 類似度

        result = None
        if attr_index is None:
            result = ItemMappingResult(
                attr_index,
                message="{}を追加".format(target_attr_name),
                filter_key="insert_col",
                filter_params=json.dumps({"output_attr_name": target_attr_name,
                                          "output_attr_new_index": target_attr_index, }),
            )
        elif target_attr_index is None:
            result = ItemMappingResult(
                attr_index,
                message="{}を削除".format(attr_name),
                filter_key="delete_col",
                filter_params=json.dumps({"input_attr_idx": attr_index, }),
            )
        elif attr_name != target_attr_name:
            result = ItemMappingResult(
                attr_index,
                message="列名を{}を{}に変更".format(attr_name, target_attr_name),
                filter_key="rename_col",
                filter_params=json.dumps({"new_col_name": target_attr_name, "input_attr_idx": attr_index, }),
            )
        # elif attr_index != target_attr_index:
        #   result = ItemMappingResult(
        #     attr_index,
        #     message="{}を{}列目に移動".format(attr_name, target_attr_index+1),
        #     filter_key = "move_col",
        #     filter_params = json.dumps({
        #       "input_attr_idx": attr_index,
        #       "output_attr_new_index": target_attr_index,
        #     }),
        #   )

        if result is not None:
            suggests.append(result)

    return suggests


def item_mapping_insert(dataset, target_dataset):
    attr_names = dataset.attr_names
    target_attr_names = target_dataset.attr_names

    suggests = []

    new_column_names = [name for name in target_attr_names if name not in attr_names]

    if len(new_column_names) == 0:
        return suggests

    suggests.append(
        ItemMappingResult(
            None,
            message="足りない列を一括追加",
            filter_key="insert_col_list",
            filter_params=json.dumps({"new_name_list": new_column_names, "target_col": len(attr_names), }),
        )
    )

    # for index, target_attr_name in enumerate(new_column_names):
    #   result = ItemMappingResult(
    #     None,
    #     message="{}を追加".format(target_attr_name),
    #     filter_key = "insert_col",
    #     filter_params = json.dumps({
    #       "new_name": target_attr_name,
    #       "target_col": index,
    #     }),
    #   )
    #   suggests.append(result)
    return suggests


def item_mapping_position(dataset, target_dataset):
    attr_names = dataset.attr_names
    target_attr_names = target_dataset.attr_names
    if attr_names == target_attr_names:
        return []

    result = ItemMappingResult(
        None,
        message="すべての列の位置を合わせる",
        filter_key="sort_col",
        filter_params=json.dumps({"input_attr_idx_names": target_dataset.attr_names}),
    )
    return [result]
