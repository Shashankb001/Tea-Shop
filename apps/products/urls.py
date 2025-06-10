from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category/<slug:category_slug>/products/', views.ProductListView.as_view(), name='product_list_by_category'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
] 