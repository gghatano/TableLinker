import logging
import random
import uuid
from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from graphql import GraphQLError
from shared.cipher import AESCipher

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    """ユーザーマネージャー."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """メールアドレスでの登録を必須にする"""
        if not email:
            raise ValueError("The given email must be set")  # TODO: 国際化
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """is_staff(管理サイトにログインできるか)と、is_superuer(全ての権限)をFalseに"""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """スーパーユーザーは、is_staffとis_superuserをTrueに"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル."""

    cipher = AESCipher("cthTUEstfg890CVfA7LKjV6ThuwkwHCRom5Pki0Dg1IGoeqIt3")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(_("email"), unique=True)
    name = models.CharField(_("name"), max_length=40, blank=True)

    is_staff = models.BooleanField(_("staff status"), default=False, help_text=_("スタッフユーザ"),)
    is_system = models.BooleanField(_("system status"), default=False, help_text=_("システムユーザ"),)
    is_active = models.BooleanField(_("active"), default=True, help_text=_("アクティブユーザ"),)

    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)
    password_reset_token = models.CharField(_("password_reset_token"), max_length=128, blank=True, null=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return self.name

    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.name

    def email_user(self, subject, html_message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, "", from_email, [self.email], html_message=html_message, **kwargs)

    @property
    def username(self):
        """username getter
        usernameは、emailにする
        """
        return self.email

    def password_reset_request(self, email):
        password_reset_token = None
        while True:
            password_reset_token = random.randint(10000, 99999)
            exist_user = User.objects.filter(password_reset_token=User.cipher.encrypt(str(password_reset_token)))
            if not exist_user:
                break
        self.password_reset_token = User.cipher.encrypt(str(password_reset_token))
        self.save()

        try:
            subject = settings.PASSWORD_RESET_SUBJECT
            from_email = settings.DEFAULT_FROM_EMAIL

            send_mail(
                subject=subject,
                message=render_to_string("mail/password_reset.txt", {"password_reset_token": password_reset_token}),
                from_email=from_email,
                recipient_list=[email],
            )
        except SMTPException:
            logger.error("UserID:{0}の方の、パスワードリセットのメール送信が失敗しています".format(self.id))

    @classmethod
    def password_reset(cls, password_reset_token, password):
        user = User.objects.filter(password_reset_token=User.cipher.encrypt(password_reset_token))
        if not user:
            raise GraphQLError("対象のユーザが存在しません")

        user = user[0]
        user.password_reset_token = None
        user.password = make_password(password)
        user.save()
        return user
