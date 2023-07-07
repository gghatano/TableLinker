from django.db import models
import numpy as np

#from datasets.utils.similar_search import SimilarSearch
from datasets.item_mapping.mapping import similarity
from shared.utils import batch_qs


class DatasetSimliar(object):
    """
    データセットの類似検索の結果
    """

    def __init__(self, sim=None, dataset_group=None):
        self.sim = sim
        self.dataset_group = dataset_group


class DatasetSimilarSearchMixin(models.Model):
    """
    類似検索のMixin
    """

    class Meta:
        abstract = True

    word_vec_bin = models.BinaryField(verbose_name="WordVecのバイナリデータ", null=True)

    @property
    def word_vec(self):
        if self.word_vec_bin is None:
            return None
        else:
            return np.frombuffer(self.word_vec_bin, "float32")

    def similar_search_text(self):
        """
        検索対象のテキストをコンマ区切りで返す
        """
        raise RuntimeError("no impl")

    def get_similar_word_vec(self):
        """
        検索対象のテキストから、Word2Vecの結果を返す
        """
        text = self.similar_search_text()
        return similarity.item2vec(text)

    def set_word_vec(self):
        """
        Word2Vecの結果を保存
        """
        vec = self.get_similar_word_vec()
        self.word_vec_bin = vec.tobytes()


class DatasetGroupSimilarSearchMixin(models.Model):
    """
    類似検索のMixin
    """

    class Meta:
        abstract = True

    def simliar_datasets(self, keyword=None, limit=None):
        """
        類似データセット検索
        """

        # 検索対象のDataset
        # TODO 公開済みかつDatasetGroupに所属しているかどうかチェック
        dataset_groups = self.__class__.objects.all().analyzed().latest().exclude(pk=self.id).distinct().with_attrs()

        if keyword is not None:
            dataset_groups = dataset_groups.search(keyword)

        # 類似検索
        word_vec = self.current_dataset.word_vec

        candidates = []
        for _, _, _, qs in batch_qs(dataset_groups):
            for dataset_group in qs:
                dataset = dataset_group.current_dataset
                if dataset is None:
                    continue  # FIXME 応急処置
                if dataset.word_vec is None:
                    continue
                candidate = DatasetSimliar(
                    sim=similarity.cos_sim(
                        word_vec, dataset.word_vec
                    ),
                    dataset_group=dataset_group,
                )
                candidates.append(candidate)

        # 類似度順にソート
        candidates.sort(key=lambda simliar: simliar.sim, reverse=True)

        if limit is not None:
            candidates = candidates[:limit]

        return candidates
