"""eCommerceWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from apps.cart.views import cart_detail, success
from apps.cart.webhook import webhook
from apps.core.views import frontpage, contact, about
from apps.coupon.api import api_can_use
from apps.newsletter.api import api_add_subscriber
from apps.order.views import admin_order_pdf
from apps.store.api import api_add_to_cart, api_remove_from_cart, api_checkout, create_checkout_session
from apps.store.views import product_detail, category_detail, search
from apps.userprofile.views import signup, myaccount, password_change_done, update_user
from .sitemaps import StaticViewSitemap, CategorySitemap, ProductSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'product': ProductSitemap,
    'category': CategorySitemap
}

urlpatterns = [
                  path('admin/admin_order_pdf/<int:order_id>/', admin_order_pdf, name='admin_order_pdf'),
                  path('admin/', admin.site.urls),

                  # Frontpage

                  path('search/', search, name='search'),
                  path('cart/', cart_detail, name='cart'),
                  path('hooks/', webhook, name='webhook'),
                  path('cart/success/', success, name='success'),
                  path('', frontpage, name='frontpage'),
                  path('contact/', contact, name='contact'),
                  path('about/', about, name='about'),

                  # Auth
                  path('myaccount/', myaccount, name='myaccount'),
                  path('signup/', signup, name='signup'),
                  path('login/', views.LoginView.as_view(template_name='login.html'), name='login'),
                  path('logout/', views.LogoutView.as_view(), name='logout'),
                  path('myaccount/password_reset/',
                       views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
                  path('myaccount/password_reset/done/',
                       views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
                       name='password_reset_done'),
                  path('myaccount/password_reset/<uidb64>/<token>/',
                       views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
                       name='password_reset_confirm'),
                  path('myaccount/reset/done',
                       views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
                       name='password_reset_complete'),
                  path('myaccount/change_password/',
                       views.PasswordChangeView.as_view(template_name='change_password.html'),
                       name='change_password'),
                  path('myaccount/change/done', password_change_done, name='password_change_done'),
                  path('myaccount/update_information', update_user, name='update_information'),

                  path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

                  # API

                  path('api/can_use/', api_can_use, name='api_can_use'),
                  path('api/create_checkout_session/', create_checkout_session, name='create_checkout_session'),
                  path('api/add_to_cart/', api_add_to_cart, name='api_add_to_cart'),
                  path('api/remove_from_cart/', api_remove_from_cart, name='api_remove_from_cart'),
                  path('api/checkout/', api_checkout, name='api_checkout'),
                  path('api/add_subscriber/', api_add_subscriber, name='api_add_subscriber'),

                  # Store

                  path('<slug:category_slug>/<slug:slug>/', product_detail, name='product_detail'),
                  path('<slug:slug>/', category_detail, name='category_detail'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
