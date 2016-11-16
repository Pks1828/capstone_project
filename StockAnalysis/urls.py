from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^search/', views.search, name="search"),
    url(r'^search_stocks/', views.search_stocks, name="search_stocks"),
    url(r'^report/', views.report, name="report"),
    url(r'^glossary/', views.glossary, name="glossary"),
    url(r'^performance/', views.performance, name="performance"),
]