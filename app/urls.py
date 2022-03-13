from django.conf.urls import url
from . import views
 
app_name = 'app'
urlpatterns = [
    url('index/', views.IndexView.as_view(), name='index'),
]
"""
url('index', views.IndexView.as_view(), name='index') 
第一引数：アクセスされるURLの定義
第二引数：URLにアクセスされた時に呼び出されるViewを定義
"""