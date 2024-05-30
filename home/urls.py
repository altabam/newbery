from django.urls import path
from home import views
urlpatterns = [
    path("", views.render_home, name="index"),
    path("tablasParametricas", views.tablasParametricas, name="tablasParametricas"),
    path("listados", views.listados, name="listados"),
]