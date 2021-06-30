from django.urls import path
from django.contrib.auth.views import (
    LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView,
)
from django.contrib.auth.decorators import login_required

import keep.apps
from keep import views

app_name = keep.apps.KeepConfig.name  # regisers the namespace so we use it for URL generation

urlpatterns = [
    path('', login_required(views.PasswordListView.as_view()), name='index'),
    path('add/', login_required(views.PasswordCreateView.as_view()), name='add'),
    path('update/<pk>', login_required(views.PasswordUpdateView.as_view()), name='update'),
    path('delete/<pk>', login_required(views.PasswordDeleteView.as_view()), name='delete'),

    path('category', login_required(views.CategoryListView.as_view()), name='category'),
    path('category/add/', login_required(views.CategoryCreateView.as_view()), name='category_add'),
    path('category/update/<pk>', login_required(views.CategoryUpdateView.as_view()), name='category_update'),
    path('category/delete/<pk>', login_required(views.CategoryDeleteView.as_view()), name='category_delete'),

    path('profile/', login_required(views.Profile.as_view()), name='profile'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('register_email_sent/', views.RegisterEmailSent.as_view(), name='register_email_sent'),
    path('activate_user/<uidb64>/<token>', views.ActivateUser.as_view(), name='activate_user'),
    path('password_change/', login_required(PasswordChangeView.as_view(success_url='done/')), name="password_change"),
    path('password_change/done/', login_required(PasswordChangeDoneView.as_view()), name="password_change_done"),
    path('password_reset/', PasswordResetView.as_view(success_url='done/'), name="password_reset"),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(success_url='/reset/done/'),
         name="password_reset_confirm"),  # /reset/MQ/set-password/
    path('reset/done/', PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]
