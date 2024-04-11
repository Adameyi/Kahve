from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from .views import IndexView, FavouritesListView

urlpatterns = [
    # URL patterns for serving media files
    path("media/<path>", serve, {"document_root": settings.MEDIA_ROOT}),
    
    # URL patterns for serving static files
    path("static/<path>", serve, {"document_root": settings.STATIC_ROOT}),
    
    path("", views.index, name='index'),
    path("", IndexView.as_view(), name='index'),
    path("favourites/", FavouritesListView.as_view(), name='favourites'),
    path("favourites/<int:product_id>/", views.favourite_product, name="favourite_product"),
    path("add_category", views.add_category, name='add_category'),
    path('buy_product/<int:product_id>/', views.buy_product, name='buy_product'),
    
    # Filter
    path('search/', views.search_products, name='search_products'),
    
    # Admin URLs
    path("add/", views.add_product, name="add_product"),
    path("admin/", views.index, name="admin_index"),
    path("admin/", IndexView.as_view(), name="admin_index"),
    path("admin/delete/<int:product_id>", views.delete_product, name="delete_product"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
