from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.signin,name="signin"),
    path("signup", views.signup, name="signup"),
    path("home",views.home,name="home"),
    path("logout",views.logout_user,name="logout"),
    path("profile",views.profile,name="profile"),
    path("myQuestion",views.myQuestion,name="myQuestion"),
    path("allQuestion",views.allQuestion,name="allQuestion"),
    path("askQuestion",views.askQuestion,name="askQuestion"),
    path("markanswer",views.MarkAnswer.as_view(),name="markanswer"),
    path("getanswer",views.GetAnswer.as_view(),name="getanswer"),
]
   