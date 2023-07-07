from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("users/create", views.UserCreate.as_view(), name="create"),
    path("users/create/done", views.UserCreateDone.as_view(), name="create_done"),
    path("users/create/complete/<token>/", views.UserCreateComplete.as_view(), name="create_complete",),
    path("users", views.UserDetail.as_view(), name="detail"),
    path("users/edit", views.UserUpdate.as_view(), name="update"),
    path("password/change", views.PasswordChange.as_view(), name="password_change",),
    path("password_reset/", views.PasswordReset.as_view(), name="password_reset"),
    path("password_reset/done/", views.PasswordResetDone.as_view(), name="password_reset_done",),
    path("password_reset/confirm/<uidb64>/<token>/", views.PasswordResetConfirm.as_view(), name="password_reset_confirm",),
    path("password_reset/complete/", views.PasswordResetComplete.as_view(), name="password_reset_complete",),
    path("email/change/", views.EmailChange.as_view(), name="email_change"),
    path("email/change/done/", views.EmailChangeDone.as_view(), name="email_change_done",),
    path("email/change/complete/<str:token>/", views.EmailChangeComplete.as_view(), name="email_change_complete",),
]
