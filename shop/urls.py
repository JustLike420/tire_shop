from django.urls import path

from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    OrderSummeryView
)

urlpatterns = [
    path('list/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('update/<int:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name='product_delete'),

    path('order/', OrderSummeryView.as_view(), name='order'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('remove-single-item-from-cart/<int:pk>/', remove_single_item_from_cart,
         name='remove_single_item_from_cart'),

]
