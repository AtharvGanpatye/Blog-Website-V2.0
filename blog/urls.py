from django.urls import path
from blog import views
from blog.views import PostListView, PostDeleteView, UserPostListView, PostCreateView, PostUpdateView
#PostDetailView
app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='blogHome'),
    path('posts/<username>/', UserPostListView.as_view(), name='user_posts'),
    path('<int:pk>/', views.blogPost, name='blogPost'),
    path('profile/', views.profile, name='profile'),
    path('new/', PostCreateView.as_view(), name='new'),
    path('post_update/<int:pk>/', PostUpdateView.as_view(), name="post_update"),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='delete'),
    path('comment/<int:sno>/', views.comment, name="comment")
]

# Class Based Views Look ForThe Below Template By Default:
# <appname>/<model>_<viewtype>.html
# path('<int:pk>/', PostDetailView.as_view(), name='blogPost')
# path('new/', views.new, name='new')
# path('post_update/<int:sno>/', views.post_update, name="post_update")