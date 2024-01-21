from django.urls import path
from .views import (HomeView, ArticleDetail, AddPostView, UpdatePostView, DeletePostView,
                    AddCategoryView, CategoryView, CategoryListView, LikeView, AddCommentView, post_list)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('article/<int:pk>/', ArticleDetail.as_view(), name='article_detail'), # <int:pk> integer, primary key of the post
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('article/edit/<int:pk>/', UpdatePostView.as_view(), name='update_post'), # знову беремо primary key підтягувати id з бази даних
    path('article/<int:pk>/remove', DeletePostView.as_view(), name='delete_post'),
    path('category/<str:cats>/', CategoryView, name='category'),
    path('category-list/', CategoryListView, name='category-list'),
    path('like/<int:pk>/', LikeView, name='like_post'),
    path('article/<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('search/', post_list, name='search'),
]
