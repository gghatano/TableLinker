class BulamFormMixin(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "input"
            field.widget.attrs["placeholder"] = field.label  # placeholderにフィールドのラベルを入れ
