from django.urls import path
from . import views


urlpatterns = [
    path('wishlists/', views.wishlists_list),
    path('wishlists/<int:pk>', views.wishlists_detail),
    path('wishlists/<int:wishlist_id>/products/<int:product_id>', views.wishlists_product),
]
