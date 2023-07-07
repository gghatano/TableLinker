from enum import Enum


class PublicLevel(Enum):
    public = (100, "公開中")
    # insite = (50, "ログイン済みユーザのみ公開")
    private = (10, "非公開")

    @classmethod
    def get_value(cls, member):
        return cls[member].value[0]

    @classmethod
    def get_name(cls, value):
        for member in list(PublicLevel):
            if value == member.value[0]:
                return member.value[1]
