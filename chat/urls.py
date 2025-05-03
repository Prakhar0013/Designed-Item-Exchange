from django.urls import path
from . import views

# app_name = 'chat'

urlpatterns = [
    path('start/<int:item_id>/', views.start_or_go_to_chat, name='start_chat'),
    path('room/<int:room_id>/', views.ChatRoomView.as_view(), name='chat_room'),
    path('list/', views.ChatListView.as_view(), name='chat_list'),
]