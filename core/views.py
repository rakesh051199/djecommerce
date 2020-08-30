import stripe
import string
import random
from django.shortcuts import render,get_object_or_404,redirect
from .models import item,orderitem,order,Address,Payment,coupon,requestrefund,Userprofile
from django.views.generic import ListView,DetailView,View
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import checkoutform,couponform,refundform,PaymentForm
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY

def get_refcode():
    return ''.join(random.choices(string.ascii_lowercase+string.digits,k=20))

def is_valid_form(values):
    valid=True
    for field in values:
        if field=='':
            valid=False
    return valid



# Create your views here.
class Homeview(ListView):
    model=item
    paginate_by = 1000
    template_name = "home-page.html"

class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            Order=order.objects.get(user=self.request.user,ordered=False)
            context={
                'object':Order
            }
            return render(self.request,'order-summary.html',context)
        except ObjectDoesNotExist:
            messages.warning(self.request,"The item was not present")
            return redirect("/")

class itemdetail(DetailView):
    model=item
    template_name = "product-page.html"

class checkoutview(View):
    def get(self,*args,**kwargs):
        try:
            Order=order.objects.get(user=self.request.user,ordered=False)
            form=checkoutform()
            context={
            'form':form,
            'Order':Order,
            'formcoupon':couponform(),
            'display_coupon_form':True
            }
            shipping_address_qs=Address.objects.filter(
                user=self.request.user,
                default=True,
                address_type='S'

            )
            if shipping_address_qs.exists():
                context.update({'default_shipping_address':shipping_address_qs[0]})


            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update({'default_billing_address': billing_address_qs[0]})

            return render(self.request,'checkout-page.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,'you do not have an active order')
            return redirect('core:checkout')
    def post(self,*args,**kwargs):
        try:
            Order=order.objects.get(user=self.request.user,ordered=False)
            form = checkoutform(self.request.POST or None)
            print(self.request.POST)
            if form.is_valid():
                use_default_shipping=form.cleaned_data.get('use_default_shipping')
                if use_default_shipping:
                    print("using the default shipping address")
                    address_qs=Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address=address_qs[0]
                        Order.shipping_address=shipping_address
                        Order.save()
                    else:
                        messages.info(self.request,'no default shipping addresses are available')
                        return redirect('core:checkout')
                else:
                    print('user is entering a new shipping address')
                    shipping_address1= form.cleaned_data.get('shipping_address')
                    shipping_address2= form.cleaned_data.get('shipping_address2')
                    shipping_country = form.cleaned_data.get('shipping_country')
                    shipping_zip= form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1,shipping_address2,shipping_country,shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            address=shipping_address2,
                            country=shipping_country ,
                            zipcode=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()
                        Order.shipping_address = shipping_address
                        Order.save()

                        set_default_shipping = form.cleaned_data.get('set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(self.request,'please fill the required shipping address filds')

                use_default_billing=form.cleaned_data.get('use_default_billing')
                same_billing_address=form.cleaned_data.get('same_billing_address')

                if same_billing_address:
                    billing_address=shipping_address
                    billing_address.pk=None
                    billing_address.save()
                    billing_address.address_type='B'
                    billing_address.save()
                    Order.billing_address=billing_address
                    Order.save()
                elif use_default_billing:
                    print("using the default shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        Order.billing_address=billing_address
                        Order.save()
                    else:
                        messages.info(self.request, 'no default shipping addresses are available')
                        return redirect('core:checkout')
                else:
                    print('user is entering a new billing address')
                    billing_address1 = form.cleaned_data.get('billing_address')
                    billing_address2 = form.cleaned_data.get('billing_address2')
                    billing_country = form.cleaned_data.get('billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_address2, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            address=billing_address2,
                            country=billing_country,
                            zipcode=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()
                        Order.billing_address = billing_address
                        Order.save()

                        set_default_billing = form.cleaned_data.get('set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(self.request, 'please fill the required shipping address filds')
                payment_option = form.cleaned_data.get('payment_option')
                if payment_option == 'S':
                    return redirect('core:payment')
                elif payment_option == 'P':
                    return redirect('core:payment')
                else:
                    messages.warning(self.request, "Invalid payment option selected")
                    return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:order-summary")



class paymentview(View):
    def get(self,*args,**kwargs):
        Order = order.objects.get(user=self.request.user,ordered=False)
        if Order.billing_address:
            context = {
                'Order': Order,
                'formcoupon': couponform(),
                'display_coupon_form': False,
                'form':PaymentForm()
            }
            userprofile=self.request.user.userprofile
            if userprofile.one_click_purchasing:
                # fetch the users card list
                cards = stripe.Customer.list_sources(
                    userprofile.stripe_customer_id,
                    limit=3,
                    object='card'
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    # update the context with the default card
                    context.update({'card': card_list[0]})
            return render(self.request, 'payment.html', context)
        else:
            messages.warning(self.request,'you do not have a billing address')
            return redirect('core:checkout')
    def post(self,*args,**kwargs):
        Order=order.objects.get(user=self.request.user,ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = Userprofile.objects.get(user=self.request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id)
                    customer.sources.create(source=token)

                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                    )
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()
        amount =int( Order.get_total())
        try:
            if use_default or save:
                charge = stripe.Charge.create(
                    amount=amount,  # cents
                    currency="INR",
                    customer=userprofile.stripe_customer_id,
                )
            else:
                # charge once off on the token
                charge = stripe.Charge.create(
                    amount=amount,  # cents
                    currency="INR",
                    source=token
                )

            # creating the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = Order.get_total()
            payment.save()

            order_item = Order.items.all()
            order_item.update(ordered=True)
            for it in order_item:
                it.save()
            # assigning payment to the order
            Order.ordered = True
            Order.payment = payment
            # TODO:add ref_code
            Order.ref_code = get_refcode()

            Order.save()
            messages.success(self.request, 'your order was successfull')
            return redirect('/')

        except stripe.error.CardError as e:
            print(e)
            body=e.json_body
            err=body.get('error',{})
            messages.error(self.request,f"{err.get('message')}")
            return redirect('/')
        except stripe.error.RateLimitError as e:
            print(e)
            # Too many requests made to the API too quickly
            messages.error(self.request, "rate limit error")
            return redirect('/')

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            print(e)
            messages.error(self.request, "invalid parametres")
            return redirect('/')

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            print(e)
            messages.error(self.request, "Not authenticated")
            return redirect('/')

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            print(e)
            messages.error(self.request, "Network error")
            return redirect('/')

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            print(e)
            messages.error(self.request, "something went wrong,you were not charged,try again")
            return redirect('/')

        except Exception as e:
            # Send to email yourselves
            print(e)
            messages.error(self.request, "a serious error occured,you have been notified")
            return redirect('/')

        messages.warning(self.request, "Invalid data received")
        return redirect("core:payment")



def add_item_cart(request,slug):
    Item=get_object_or_404(item,slug=slug)
    order_item,created=orderitem.objects.get_or_create(Item=Item,user=request.user,ordered=False)
    order_qs=order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        Order=order_qs[0]
        if Order.items.filter(Item__slug=Item.slug).exists():
            order_item.quantity+=1
            order_item.save()
            messages.info(request, "This item was updated successfully")
            return redirect('core:order-summary')
        else:
            Order.items.add(order_item)
            messages.info(request, "This item was added to cart successfully")
            return redirect('core:order-summary')
    else:
        ordered_date=timezone.now()
        Order=order.objects.create(user=request.user,ordered_date=ordered_date)
        Order.items.add(order_item)
        messages.info(request, "This item was add to cart successfully")
        return redirect('core:order-summary')

def remove_from_cart(request,slug):
    Item=get_object_or_404(item,slug=slug)
    order_qs=order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        Order=order_qs[0]
        #check if order item is in the order
        if Order.items.filter(Item__slug=Item.slug).exists():
            order_item=orderitem.objects.filter(Item=Item,user=request.user,ordered=False)[0]
            Order.items.remove(order_item)
            order_item.delete()
            messages.info(request,"This item was removed from your cart")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product",slug=slug)
    else:
        messages.info(request, "you do not have an active order")
        return redirect("core:product",slug=slug)
def remove_single_item_from_cart(request,slug):
    Item=get_object_or_404(item,slug=slug)
    order_qs=order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        Order=order_qs[0]
        #check if order item is in the order
        if Order.items.filter(Item__slug=Item.slug).exists():
            order_item=orderitem.objects.filter(Item=Item,user=request.user,ordered=False)[0]
            if order_item.quantity>1:
                order_item.quantity-=1
                order_item.save()
            else:
                Order.items.remove(order_item)
            messages.info(request,"This item quantity was updated")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product",slug=slug)
    else:
        messages.info(request, "you do not have an active order")
        return redirect("core:product",slug=slug)

def get_coupon(request,code):
    try:
        Code=coupon.objects.get(code=code)
        return Code
    except ObjectDoesNotExist:
        messages.warning(request,"The coupon does not exist")
        return redirect("core:checkout")




class addcouponview(View):
        def post(self, *args, **kwargs):
            form = couponform(self.request.POST or None)
            if form.is_valid():
                try:
                    code = form.cleaned_data.get('code')
                    Order = order.objects.get(user=self.request.user, ordered=False)
                    Order.dis_coupon = get_coupon(self.request, code)
                    Order.save()
                    messages.success(self.request, 'successfully coupon added')
                    return redirect('core:checkout')
                except ObjectDoesNotExist:
                    messages.warning(self.request, "you do not have an active order")
                    return redirect("core:checkout")

class refundview(View):
    def get(self,*args,**kwargs):
        form=refundform()
        context={
            'form':form
        }
        return render(self.request,'refund.html',context)
    def post(self,*args,**kwargs):
        form=refundform(self.request.POST)
        if form.is_valid():
            ref_code=form.cleaned_data.get('ref_code')
            message=form.cleaned_data.get('message')
            email=form.cleaned_data.get('email')
            #edit the order

            try:
                Order=order.objects.get(ref_code=ref_code)
                Order.refund_requested=True
                Order.save()
                #start the refund
                refund=requestrefund()
                refund.Order=Order
                refund.reason=message
                refund.email=email
                refund.save()

                messages.info(self.request,'your request was accepted')
                return redirect('core:infpage',pk=refund.pk)
            except ObjectDoesNotExist:
                messages.info(self.request,'you do not have ref code')
                return redirect('core:refund')
def infview(request,pk):
    ree=requestrefund.objects.get(pk=pk)
    context={
        'req':ree
    }
    return render(request,'information.html',context)



















