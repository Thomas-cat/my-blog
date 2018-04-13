from django.urls import path
from . import views
app_name = 'blog'

# (?p是匹配捕捉的正则表达式，命名name = ‘’ 是为了在 反解析app:app_name 里起作)
urlpatterns = [
	path('',views.index,name = 'index'),
	path(r'post/<int:pk>/',views.detail,name = 'detail'),
	path('archives/<int:year>/<int:month>/',views.archives,name = 'archives'),
	path('category/<int:pk>',views.category,name = 'category'),
]
