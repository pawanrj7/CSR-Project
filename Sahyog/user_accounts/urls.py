from django.urls import path, include
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user_accounts import views as user_views
from django.conf.urls import url
from . import views

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(
        template_name='user_accounts/new.html'),name='login'),
    path('register/', views.register, name='register'),
    path('email_verification/',views.email_verify,name='email_verify'),
    path('logout/', views.user_logout, name='logout'),
    path('user_login/', views.user_login, name='user_login'),
    path('complogin/', views.comp_login, name='user_login'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('profile_update/<int:pk>/', views.profile_update, name='profile_update'),
    # path('index/', include( 'user_accounts'), name='index'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='user_accounts/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='user_accounts/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='user_accounts/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='user_accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

]

