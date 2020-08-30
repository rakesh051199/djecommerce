from django.urls import path
from core import views
from django.conf.urls.static import static
from django.conf import settings

app_name='core'

urlpatterns=[
    path('',views.Homeview.as_view(),name="item-list"),
    path('ordersummary/',views.OrderSummaryView.as_view(),name="order-summary"),
    path('product/<slug>',views.itemdetail.as_view(),name="product"),
    path('add_to_cart/<slug>',views.add_item_cart,name="add-to-cart"),
    path('add_coupon/',views.addcouponview.as_view(),name="add_coupon"),
    path('remove_from_cart/<slug>',views.remove_from_cart,name="remove-from-cart"),
    path('checkout/',views.checkoutview.as_view(),name="checkout"),
    path('remove_single_item_from_cart/<slug>',views.remove_single_item_from_cart,name="remove-single-cart"),
    path('payment/',views.paymentview.as_view(),name="payment"),
    path('refund/',views.refundview.as_view(),name="refund"),
    path('success/<pk>',views.infview,name="infpage"),

]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
