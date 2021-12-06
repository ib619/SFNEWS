from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostCreateView, PostUpdateView, PostDeleteView, CategoryView
from .views import CategoryUnsubView

urlpatterns = [
    path('news/', (PostList.as_view()), name='posts'),
    path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='posts_search'),
    path('news/add', PostCreateView.as_view(), name='post_create'),
    path('news/<int:pk>/edit', PostUpdateView.as_view(), name='post_update'),
    path('news/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('news/category/sub/<int:pk>', CategoryView.as_view(), name='category_subscribe'),
    path('news/category/unsub/<int:pk>', CategoryUnsubView.as_view(), name='category_unsub'),
]