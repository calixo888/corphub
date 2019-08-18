from django.conf.urls import url
from corphub_app import views

app_name = "corphub_app"

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^view-all/', views.viewall, name="view_all"),
]
