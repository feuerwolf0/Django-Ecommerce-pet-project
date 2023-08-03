from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.registration_view, name='signup'),
    path('profile/addresses/set_main/<int:aid>', views.select_main_address, name='set_main'),
    path('profile/addresses/change_address/<int:aid>', views.change_address, name='change_address'),
    path('profile/addresses/delete_address/<int:aid>', views.delete_address, name='delete_address'),
    path('profile/addresses/add_address/', views.create_address, name='create_address'),
    path('profile/addresses/', views.addresses_view, name='addresses'),
    path('profile/activity/', views.activity_view, name='activity'),
    path('profile/security/', views.profile_security_view, name='security'),
    path('profile/', views.profile_view, name='profile'),
    path('recovery/<uidb64>/<token>', views.PasswordRecoveryConfirmView.as_view(), name='recovery_confirm'),
    path('recovery/done/', views.PasswordRecoveryDoneView.as_view(), name='recovery_done'),
    path('recovery/', views.PasswordRecoveryView.as_view(), name='recovery'),
]