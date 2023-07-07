from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.signing import BadSignature, SignatureExpired, dumps, loads
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, resolve_url
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic

from .forms import (
    EmailChangeForm,
    LoginForm,
    MyPasswordChangeForm,
    MyPasswordResetForm,
    MySetPasswordForm,
    UserCreateForm,
    UserUpdateForm,
)

#  from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class Login(LoginView):
    """
    ログインページ
    """

    form_class = LoginForm
    template_name = "users/login.html"


class Logout(LoginRequiredMixin, LogoutView):
    """
    ログアウトページ
    """


class RequiredLoginMixin(UserPassesTestMixin):
    # 権限チェックで落ちた場合に403ページへ飛ぶ
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user is not None or user.is_superuser


class UserCreate(generic.CreateView):
    """ユーザー登録"""

    template_name = "users/create.html"
    form_class = UserCreateForm

    def form_valid(self, form):
        # 認証メールなし
        # user = form.save(commit=False)
        # user.is_active = True
        # user.save()
        #
        # login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        # messages.success(self.request, _('success create user'))
        #
        # return redirect('dashboard:top')  # TODO: ユーザ登録後のリダイレクト先

        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            "protocol": self.request.scheme,
            "domain": domain,
            "token": dumps(user.pk),
            "user": user,
        }

        subject = render_to_string("users/mail/create/subject.txt", context)
        message = render_to_string("users/mail/create/message.html", context)

        user.email_user(subject, message)
        return redirect("users:create_done")


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""

    template_name = "users/create_done.html"


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""

    template_name = "users/create_complete.html"
    timeout_seconds = getattr(settings, "ACTIVATION_TIMEOUT_SECONDS", 60 * 60 * 24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get("token")
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()

                    # login(
                    #     request,
                    #     user,
                    #     backend="django.contrib.auth.backends.ModelBackend",
                    # )
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


class UserDetail(RequiredLoginMixin, generic.DetailView):
    """マイページ"""

    model = User
    template_name = "users/detail.html"

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)


class UserUpdate(RequiredLoginMixin, SuccessMessageMixin, generic.UpdateView):
    """ユーザ情報編集"""

    model = User
    form_class = UserUpdateForm
    template_name = "users/update.html"
    success_message = "ユーザ情報を変更しました。"

    def get_success_url(self):
        return resolve_url("users:detail")

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)


class PasswordChange(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    """パスワード変更ビュー"""

    form_class = MyPasswordChangeForm
    success_url = reverse_lazy("users:detail")  # TOOD: パスワード変更後の遷移先
    template_name = "users/password_change.html"
    success_message = "パスワードを変更しました。"


class EmailChange(LoginRequiredMixin, SuccessMessageMixin, generic.FormView):
    """メールアドレスの変更"""

    template_name = "users/email_change_form.html"
    form_class = EmailChangeForm
    success_url = reverse_lazy("users:detail")
    success_message = "メールアドレスに確認メールを送信しました。"

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data["email"]

        # URLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            "protocol": "https" if self.request.is_secure() else "http",
            "domain": domain,
            "token": dumps(new_email),
            "user": user,
        }

        subject = render_to_string("users/mail/email_change/subject.txt", context)
        message = render_to_string("users/mail/email_change/message.html", context)
        send_mail(subject, message, None, [new_email])

        return super().form_valid(form)


class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""

    subject_template_name = "users/mail/password_reset/subject.txt"
    email_template_name = "users/mail/password_reset/message.html"
    template_name = "users/password_reset_form.html"
    form_class = MyPasswordResetForm
    success_url = reverse_lazy("users:password_reset_done")


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""

    template_name = "users/password_reset_done.html"


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""

    form_class = MySetPasswordForm
    success_url = reverse_lazy("users:password_reset_complete")
    template_name = "users/password_reset_confirm.html"


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""

    template_name = "users/password_reset_complete.html"


class EmailChangeDone(LoginRequiredMixin, generic.TemplateView):
    """メールアドレスの変更メールを送ったよ"""

    template_name = "users/email_change_done.html"


class EmailChangeComplete(LoginRequiredMixin, generic.TemplateView):
    """リンクを踏んだ後に呼ばれるメアド変更ビュー"""

    template_name = "users/email_change_complete.html"
    timeout_seconds = getattr(settings, "ACTIVATION_TIMEOUT_SECONDS", 60 * 60 * 24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        token = kwargs.get("token")
        try:
            new_email = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            User.objects.filter(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()
            return super().get(request, **kwargs)
