from django.urls import path
from cobros import views
urlpatterns = [
    path("",views.render_cobros, name="cobros"),
    
]