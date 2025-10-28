from django.urls import path
from . import views

urlpatterns = [
    # Home & Auth
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Browse
    path('products/', views.browse_products, name='browse_products'),
    path('services/', views.browse_services, name='browse_services'),
    
    # Create - MUST come before detail patterns to avoid slug conflicts
    path('product/create/', views.create_product, name='create_product'),
    path('service/create/', views.create_service, name='create_service'),
    
    # My Listings - specific paths before slug patterns
    path('my/products/', views.my_products, name='my_products'),
    path('my/services/', views.my_services, name='my_services'),
    
    # Edit & Delete - UUID patterns (more specific) before slug patterns
    path('product/<uuid:pk>/edit/', views.edit_product, name='edit_product'),
    path('service/<uuid:pk>/edit/', views.edit_service, name='edit_service'),
    path('product/<uuid:pk>/delete/', views.delete_product, name='delete_product'),
    path('service/<uuid:pk>/delete/', views.delete_service, name='delete_service'),
    
    # Promotions - UUID patterns
    path('product/<uuid:pk>/promote/', views.promote_product, name='promote_product'),
    path('service/<uuid:pk>/promote/', views.promote_service, name='promote_service'),
    
    # Change Requests - UUID patterns
    path('product/<uuid:pk>/request-price-change/', views.request_price_change, name='request_price_change'),
    path('product/<uuid:pk>/request-image-change/', views.request_image_change, name='request_image_change'),
    
    # Reports - slug patterns but more specific
    path('product/<slug:slug>/report-availability/', views.report_availability, name='report_availability'),
    
    # Product Details - These should come AFTER all specific patterns
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('service/<slug:slug>/', views.service_detail, name='service_detail'),
    
    # Reviews - generic item_type pattern
    path('<str:item_type>/<slug:slug>/review/', views.add_review, name='add_review'),
    
    # Contact - generic item_type pattern
    path('<str:item_type>/<slug:slug>/contact/', views.contact_seller, name='contact_seller'),
    
    # Messages
    path('messages/', views.my_messages, name='my_messages'),
]