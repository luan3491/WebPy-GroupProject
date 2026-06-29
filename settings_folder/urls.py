"""
URL configuration for settings_folder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from ComputerGames import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('useradmin/', include('Useradmin.urls')),
    path('useradmin/', include('django.contrib.auth.urls')),
    path('', views.GameListView.as_view(), name='game_list'),
    path('<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),
    path('library/', views.game_list, name='game_list_funbasvie'),
    path('funbasvie/<int:pk>/', views.game_detail, name='game_detail_funbasvie'),
    path('comment/<int:comment_id>/<str:up_or_down>/',views.comment_vote,name='comment_vote'),
    path('review/<int:review_id>/comment/',views.add_review_comment,name='add_review_comment'),
    path('review/<int:review_id>/vote/<str:vote_type>/',views.review_vote,name='review_vote'),
    path("funbasvie/<int:pk>/pdf/",views.game_pdf,name="game_pdf"),
    path("home/", views.home, name="home"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )