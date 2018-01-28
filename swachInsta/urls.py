"""swachInsta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from home.views  import home_view,login_view,feed_view,post_view,like_view,comment_view,logout_view,user_view,upvote_view
from swachBharat.views import swachbharat_view,upload_view,wall_view,sort_view
urlpatterns = [
    url(r'^$', home_view, name="home"),
    url(r'^login/', login_view, name="login"),
    url(r'^feed/', feed_view, name="feed"),
    url(r'^post/', post_view, name="post"),
    url(r'^like/', like_view, name="like"),
    url(r'^comment/',comment_view, name="comment"),
    url(r'^swachbharat/',swachbharat_view, name="swachBharat"),
    url(r'^upload/', upload_view, name="upload"),
    url(r'^wall/', wall_view, name="wall"),
    url(r'^sort/', sort_view, name="sort"),
    url(r'^logout/', logout_view, name="logout"),
    url(r'^user=(?P<username>.+)/$', user_view,name="user"),
    url(r'^upvote/', upvote_view, name="upvote"),
]
