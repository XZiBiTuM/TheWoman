"""
URL configuration for the_woman project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path
from catalog.views import *
from django.conf import settings
from django.conf.urls.static import static
from catalog.converters import NoCommaSpaceConverter
from catalog import converters
from django.urls import path, register_converter
from django.views import defaults as default_views


register_converter(converters.NoCommaSpaceConverter, '')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('remove-from-cart/<int:product_id>/<str:color>/<str:size>', remove_from_cart, name='remove_from_cart'),
    path('erotica/<slug:slug>/<str:article>/<str:size>/', product_detail, name='product_detail'),
    path('panties/<slug:slug>/<str:article>/<str:size>/', product_detail1, name='product_detail1'),
    path('home/<slug:slug>/<str:article>/<str:size>/', product_detail2, name='product_detail2'),
    path('accessories/<slug:slug>/<str:article>/<str:size>/', product_detail3, name='product_detail3'),
    path('kaurs_laurel_mandhari_eva_lelari/<slug:slug>/<str:article>/<str:size>/', product_detail4, name='product_detail4'),
    #re_path(r'^kaurs_laurel_mandhari_eva_lelari/(?P<slug>[-\w]+)/(?P<article>[^/]+)/(?P<size>[^/]+)/$', product_detail4, name='product_detail4'),
    path('beachwear/<slug:slug>/<str:article>/<str:size>/', product_detail5, name='product_detail5'),
    path('update-cart/<int:product_id>/<str:size>', update_cart, name='update_cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='cart'),
    path('erotica/', ProductListView.as_view(), name='product_list'),
    path('panties/', ProductListView1.as_view(), name='product_list_1'),
    path('home/', ProductListView2.as_view(), name='product_list_2'),
    path('accessories/', ProductListView3.as_view(), name='product_list_3'),
    path('kaurs_laurel_mandhari_eva_lelari/', ProductListView4.as_view(), name='product_list_4'),
    path('beachwear/', ProductListView5.as_view(), name='product_list_5'),
    path('checkout/', checkout, name='checkout'),
    path('checkout/success/', checkout_success, name='checkout_success'),
    path('checkout/error/', checkout_error, name='checkout_error'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('contacts/', contacts, name='contacts'),
    path('about_us/', about_us, name='about_us'),
    path('policy/', policy, name='policy'),
    path('update_product/<int:product_id>/', update_product, name='update_product'),
    path('base_site/', transfer_folders, name='transfer_folders'),
    path('', main, name='main'),
    path('catalog/', lambda request: redirect('main'), name='redirect'),
    path('contacts.html/', lambda request: redirect('contacts'), name='redirect'),
    path('about.html/', lambda request: redirect('about_us'), name='redirect'),
    path('catalog/accessories/d002.html/', lambda request: redirect('product_list_3'), name='redirect'),
    path('catalog/kupalniki/', lambda request: redirect('product_list_5'), name='redirect'),
    path('catalog/accessories/', lambda request: redirect('product_list_3'), name='redirect'),
    path('catalog/panties/', lambda request: redirect('product_list_1'), name='redirect'),
    path('catalog/home/', lambda request: redirect('product_list_2'), name='redirect'),
    path('catalog/panties/1909.html/', lambda request: redirect('product_list_1'), name='redirect'),
    path('catalog/accessories/6202.html/', lambda request: redirect('product_list_3'), name='redirect'),
    path('catalog/kaurs-laurel-i-mandhari/1938-s.html/', lambda request: redirect('product_list_4'), name='redirect'),
    path('catalog/panties/1908.html/', lambda request: redirect('product_list_1'), name='redirect'),
    path('catalog/panties/1241.html/', lambda request: redirect('product_list_1'), name='redirect'),
    path('catalog/kaurs-laurel-i-mandhari/05207-d.html/', lambda request: redirect('product_list_4'), name='redirect'),
    path('catalog/accessories/1100.html/', lambda request: redirect('product_list_3'), name='redirect'),
    path('catalog/accessories/portupeya.html/', lambda request: redirect('product_list_3'), name='redirect'),
    path('catalog/home/8854.html/', lambda request: redirect('product_list_2'), name='redirect'),
    path('catalog/home/penyuar-eva-lelari-2364.html/', lambda request: redirect('product_list_2'), name='redirect'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler400 = default_views.bad_request
handler404 = default_views.page_not_found
handler505 = default_views.server_error