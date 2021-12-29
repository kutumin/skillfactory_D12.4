from django.contrib.auth import views
from django.urls import path, include
from .views import PostDetail, PostSearch, PostListNews, PostAdd, ProductUpdateView,PostDeleteView, IndexView, BaseRegisterView
from django.contrib.auth.views import LoginView, LogoutView
from .views import upgrade_me, subsribe_me

urlpatterns = [
    path('', PostListNews.as_view()),
    path('protected_index/', IndexView.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path ('search/', PostSearch.as_view()),
    path ('add', PostAdd.as_view()),
    path('<int:pk>/edit', ProductUpdateView.as_view(), name='update_post_detail'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('login/', LoginView.as_view(template_name = 'login.html'),name='login'),
    path('protected_index/logout/', LogoutView.as_view(template_name = 'logout.html'),name='logout'),
    path('accounts/', include('allauth.urls')),
    path('signup/', BaseRegisterView.as_view(template_name = 'signup.html'), name='signup'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('subscribe/', subsribe_me, name='new'),
]