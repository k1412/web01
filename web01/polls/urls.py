from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    # path('',views.index,name='index'),
    # # 其中name参数是为了在工程中可以在任意的地点唯一的引用它，这个有用的特性允许你只改一个文件就能全局地修改某个 URL 模式。
    # path('<int:question_id>/',views.detail,name='detail'),
    # path('<int:question_id>/results/',views.results,name='results'),
    # path('<int:question_id>/vote/',views.vote,name='vote'),
    
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]