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
from ComputerGames import views as game_views
from Shoppingcart import views as cart_views
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', game_views.home, name='home'),
    path("i18n/", include("django.conf.urls.i18n")), # internalization and localization
    path('home/', game_views.home, name='home'),

    path('useradmin/', include('Useradmin.urls')),
    path('useradmin/', include('django.contrib.auth.urls')),

    path('library/', game_views.game_list, name='game_list'),
    path('game/<int:pk>/', game_views.game_detail, name='game_detail'),
    path('game/<int:pk>/pdf/', game_views.game_pdf, name='game_pdf'),

    path("review/<int:review_id>/edit/", game_views.edit_review, name="edit_review"),
    path("review/<int:review_id>/delete/", game_views.delete_review, name="delete_review"),

    path("comment/<int:comment_id>/edit/", game_views.edit_comment, name="edit_comment"),
    path("comment/<int:comment_id>/delete/", game_views.delete_comment, name="delete_comment"),

    path('review/<int:review_id>/vote/<str:vote_type>/', game_views.review_vote, name='review_vote'),
    path('comment/<int:comment_id>/<str:up_or_down>/', game_views.comment_vote, name='comment_vote'),

    path('review/<int:review_id>/comment/', game_views.add_review_comment, name='add_review_comment'),

    path('cart/', cart_views.show_shopping_cart, name='cart'),
    path('cart/pay/', cart_views.pay, name='shopping_cart_pay'),
    path('cart/item/<int:item_id>/<str:action>/', cart_views.change_quantity, name='change_quantity'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )