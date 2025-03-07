from django.urls import path
from . import views

app_name = 'shortener'

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.url_list, name='url_list'),
    path('<str:short_code>/', views.redirect_to_url, name='redirect'),
    path('<str:short_code>/update/', views.update_url, name='update_url'),
    path('<str:short_code>/delete/', views.delete_url, name='delete_url'),
]
