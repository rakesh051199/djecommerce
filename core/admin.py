from django.contrib import admin
from .models import item,orderitem,order,Payment,coupon,requestrefund,Address,Userprofile


def make_refund_accepted(modeladmin,request,queryset):
    queryset.update(refund_requested=False,refund_granted=True)


make_refund_accepted.short_description='update orders to refund granted'


class orderadmin(admin.ModelAdmin):
    list_display = ['user','ordered','being_delivered','received','refund_requested','refund_granted','billing_address','payment','dis_coupon']
    list_filter = ['ordered','being_delivered','received','refund_requested','refund_granted']
    list_display_links = ['user','billing_address','payment','dis_coupon']
    search_fields = ['user','code']
    actions = [make_refund_accepted]

class addressadmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'address',
        'country',
        'zipcode',
        'address_type',
        'default'
    ]
    list_filter = [
        'address_type',
        'country',
        'default'
    ]
    search_fields = ['user', 'street_address', 'address', 'zipcode']


# Register your models here.
admin.site.register(item)
admin.site.register(orderitem)
admin.site.register(order,orderadmin)
admin.site.register(Payment)
admin.site.register(coupon)
admin.site.register(requestrefund)
admin.site.register(Address,addressadmin)
admin.site.register(Userprofile)

