from django.urls import path
from . import views
urlpatterns=[path('',views.home,name='home'),path('items/',views.items,name='items'),path('items/new/',views.create_item,name='create_item'),path('items/<int:pk>/',views.item_detail,name='item_detail'),path('items/<int:pk>/edit/',views.update_item,name='update_item'),path('items/<int:pk>/delete/',views.delete_item,name='delete_item'),path('feedback/',views.feedback,name='feedback'),path('api/items/',views.api_items,name='api_items'),path('api/items/<int:pk>/',views.api_item,name='api_item'),path('api/stats/',views.statistics,name='statistics')]
