from django.urls import path
from . import views

# app_name = 'items' # Optional: Use namespace if needed e.g. {% url 'items:home' %}

urlpatterns = [
    path('', views.ItemListView.as_view(), name='home'), # Home page
    path('item/new/', views.ItemCreateView.as_view(), name='item_create'),
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('item/<int:pk>/edit/', views.ItemUpdateView.as_view(), name='item_edit'),
    path('item/<int:pk>/delete/', views.ItemDeleteView.as_view(), name='item_delete'),
    path('my-posts/', views.MyPostsView.as_view(), name='my_posts'),
    # Add category view if needed: path('category/<slug:slug>/', views.CategoryItemListView.as_view(), name='category_items'),
]