from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    BaseView,
    BrandDetailView,
    ArticleDetailView,
    RegistrationView,
    LoginView,
    AccountView,
    CartView,
    AddToCardView,
    DeleteFromCartView,
    ChangeQTYView,
    AddToWishlist,
    ClearNotificationsView
)

urlpatterns = [
    # endpoints for cart
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCardView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:ct_model>/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-qty/<str:ct_model>/<str:slug>/', ChangeQTYView.as_view(), name='change_qty'),

    path('', BaseView.as_view(), name='base'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('account/', AccountView.as_view(), name='account'),
    path('clear-notifications/', ClearNotificationsView.as_view(), name='clear_notifications'),
    path('add-to-wishlist/<int:article_id>/', AddToWishlist.as_view(), name='add_to_wishlist'),
    path('<str:brand_slug>/', BrandDetailView.as_view(), name='brand_detail'),
    path('<str:brand_slug>/<str:article_slug>/', ArticleDetailView.as_view(), name='article_detail'),
]