from django.urls import path
from authe.views import Registration, login, forgetPassword, UserPasswordReset, logout

urlpatterns = [
    path('register', Registration.as_view()),
    path('login', login.as_view()),
    path('forget-password', forgetPassword.as_view()),
    path('reset-password/<uid>/<token>', UserPasswordReset.as_view()),
    path('logout', logout.as_view()),
]
