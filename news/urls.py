from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('news/create/', views.CreateView.as_view()),
    path('news/<slug:article_id>/', views.ArticleView.as_view()),
    path('news/', views.NewsView.as_view()),
    path('', views.HomeView.as_view()),
]
urlpatterns += static(settings.STATIC_URL)