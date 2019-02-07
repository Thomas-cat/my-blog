from django.urls import path
from . import views
app_name = 'blog'

# (?p是匹配捕捉的正则表达式，命名name = ‘’ 是为了在 反解析app:app_name 里起作)
urlpatterns = [
	path('',views.IndexView.as_view(),name = 'index'),
	path('post/<int:pk>/',views.PostDetailView.as_view(),name = 'detail'),
	path('archives/<int:year>/<int:month>/',views.ArchivesView.as_view(),name = 'archives'),
	path('category/<int:pk>',views.CategoryView.as_view(),name = 'category'),
	path('tag/<int:pk>',views.TagView.as_view(),name = 'tag'),
	path('recharge',views.recharge,name = 'recharge'),
	path('time_tool',views.time_tool,name = 'time_tool'),
	path('homePage',views.ccckk_homePage,name = 'homePage'),
	path('userInfo',views.ccckk_userInfo,name = 'userInfo'),
	path('detailPage',views.ccckk_detailPage,name = 'detailPage'),
	path('lottery_update',views.lottery_update),
	path('lottery_clear',views.lottery_clear),
	path('lottery_get',views.lottery_get),
#	path('search/',views.search,name = 'search'),
]
