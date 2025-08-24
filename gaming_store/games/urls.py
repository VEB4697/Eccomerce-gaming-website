# games/urls.py
from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('browse/', views.browse_view, name='browse'),
    path('<int:game_id>/', views.game_detail_view, name='game_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('discussions/', views.discussions_view, name='discussions'),
    path('<int:game_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout_view'),
    path('checkout/complete/', views.checkout_complete_view, name='checkout_complete'),
    path('invoice/', views.invoice_view, name='invoice_view'),
    path('invoice/download/', views.download_invoice_view, name='download_invoice'),
]
