from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.forms import ModelForm

from shared.forms import BulamFormMixin

#  from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class LoginForm(BulamFormMixin, AuthenticationForm):
    """ログインフォーム"""


class UserCreateForm(BulamFormMixin, UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        fields = ("email", "name")

    def clean_email(self):
        email = self.cleaned_data["email"]
        User.objects.filter(email=email, is_active=False).delete()
        return email


class UserUpdateForm(BulamFormMixin, ModelForm):
    """ユーザー情報更新フォーム"""

    class Meta:
        model = User
        fields = ("name",)


class MyPasswordChangeForm(BulamFormMixin, PasswordChangeForm):
    """パスワード変更フォーム"""


class MyPasswordResetForm(BulamFormMixin, PasswordResetForm):
    """パスワード忘れたときのフォーム"""


class MySetPasswordForm(BulamFormMixin, SetPasswordForm):
    """パスワード再設定用フォーム(パスワード忘れて再設定)"""


class EmailChangeForm(BulamFormMixin, ModelForm):
    """メールアドレス変更フォーム"""

    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data["email"]
        User.objects.filter(email=email, is_active=False).delete()
        return email
