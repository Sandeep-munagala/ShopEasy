from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name = 'home'),
    path('about/',views.about,name = 'about'),
    path('login/',views.login_user,name = 'login'),
    path('logout/',views.logout_user,name = 'logout'),
    path('register/', views.register_user, name='register'), 
    path('product/<int:pk>', views.product, name='product'), 
    path('category/<str:foo>', views.category, name='category'),
    path('cart_view', views.cart_view, name='cart_view'),
    path('add_cart<int:pk>',views.add_cart,name = "add_cart"),
    path('delete_item<int:pk>',views.delete_item,name = "delete_item"),
]