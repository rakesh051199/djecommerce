from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.db.models.signals import post_save

CATEGORY_CHOICES={
    ('s','shirt'),
    ('sw','sportswear'),
    ('ow','outwear')
}
LABEL_CHOICES={
    ('p','primary'),
    ('s','secondary'),
    ('r','danger')
}
address_choices={
    ('S','shipping'),
    ('B','billing')
}

# Create your models here.
class item(models.Model):
    title=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    price=models.FloatField()
    discount_price=models.FloatField(blank=True,null=True)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    label=models.CharField(choices=LABEL_CHOICES,max_length=1)
    slug=models.SlugField()
    description=models.TextField(max_length=300)
    quantity=models.IntegerField(default=1)
    image=models.ImageField()
    image1=models.ImageField(blank=True,null=True)

    def get_absolute_url(self):
        return reverse("core:product",kwargs={
            'slug':self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('core:add-to-cart',kwargs={
            'slug':self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse('core:remove-from-cart', kwargs={
            'slug': self.slug
        })





class orderitem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Item=models.ForeignKey(item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.Item.title}"

    def get_total_item_price(self):
        return self.quantity*self.Item.price
    def get_total_item_discount_price(self):
        return self.quantity*self.Item.discount_price
    def get_saved_amount(self):
        return self.get_total_item_price()-self.get_total_item_discount_price()
    def get_total_price(self):
        if self.Item.discount_price:
            return self.get_total_item_discount_price()
        return self.get_total_item_price()



class order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ref_code=models.CharField(max_length=30)
    items=models.ManyToManyField(orderitem)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)
    billing_address = models.ForeignKey('Address',related_name="billing" ,on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.ForeignKey('Address',related_name="shipping", on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    dis_coupon= models.ForeignKey('coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered=models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted= models.BooleanField(default=False)




    def __str__(self):
        return self.user.username
    def get_total(self):
        total=0
        for order_item in self.items.all():
            total+=order_item.get_total_price()
        if self.dis_coupon:
            total-=self.dis_coupon.amount
        return total

class Address(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    address_type=models.CharField(max_length=1,choices=address_choices)
    default=models.BooleanField(default=False)
    street_address=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    zipcode=models.CharField(max_length=100)
    country=CountryField(multiple=False)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    stripe_charge_id=models.CharField(max_length=50)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True)
    amount=models.FloatField()
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class coupon(models.Model):
    code=models.CharField(max_length=100)
    amount=models.FloatField()

    def __str__(self):
        return self.code


class requestrefund(models.Model):
    Order=models.ForeignKey('order',on_delete=models.CASCADE)
    reason=models.TextField()
    email=models.EmailField()
    accepted=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pk}"
 #storing credit card information
class Userprofile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    stripe_customer_id=models.CharField(max_length=50,blank=True,null=True)
    one_click_purchasing=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = Userprofile.objects.create(user=instance)
post_save.connect(userprofile_receiver,sender=)










