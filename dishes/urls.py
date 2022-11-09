from django.urls import path

from . import views

app_name='dishes'


urlpatterns = [
    path('', views.index, name='index'),
    path('dishes', views.leaderboard, name='leaderboard'),
    path('add-dish', views.dishAdd, name='dishAdd'),
    # path('admin/products_details/<int:dish_Id>', views.dish_details, name='dish_details'),
]