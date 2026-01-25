from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import PersonalInfo
from accounts.models import Ticket, TicketMessage

import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import uuid

def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()


        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()

    # Send order recieved email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)


# ...existing code...
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import uuid
# ...existing code...

def place_order(request, total=0, quantity=0,):
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.shipping_address = form.cleaned_data['shipping_address']
            data.social_media_link = form.cleaned_data['social_media_link']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            pi_first = request.POST.get('pi_first_name')
            if pi_first:
                try:
                    pi_birthday_raw = request.POST.get('pi_birthday','').strip()
                    pi_birthday = None
                    if pi_birthday_raw:
                        try:
                            pi_birthday = datetime.datetime.strptime(pi_birthday_raw, '%m/%d/%Y').date()
                        except ValueError:
                            try:
                                pi_birthday = datetime.datetime.strptime(pi_birthday_raw, '%Y-%m-%d').date()
                            except ValueError:
                                pi_birthday = None

                    PersonalInfo.objects.create(
                        order = data,
                        first_name = pi_first,
                        middle_name = request.POST.get('pi_middle_name',''),
                        last_name = request.POST.get('pi_last_name',''),
                        gender = request.POST.get('pi_gender',''),
                        eye_color = request.POST.get('pi_eye_color',''),
                        hair_color = request.POST.get('pi_hair_color',''),
                        birthday = pi_birthday,
                        height = request.POST.get('pi_height',''),
                        weight = (int(request.POST.get('pi_weight')) if request.POST.get('pi_weight') else None),
                        photo = request.FILES.get('pi_photo'),
                        street_address = request.POST.get('pi_street_address',''),
                        city = request.POST.get('pi_city',''),
                        zip_code = request.POST.get('pi_zip_code',''),
                    )
                except Exception as e:
                    print(f"Error saving PersonalInfo: {e}")
                    # keep view resilient; log or handle as needed
                    pass

            # Redirect to payment method selection instead of completing order
            return redirect(f'/orders/payment_method/?order_number={data.order_number}')
    else:
        return redirect('checkout')


# def place_order(request, total=0, quantity=0):
#     current_user = request.user

#     cart_items = CartItem.objects.filter(user=current_user)
#     if not cart_items.exists():
#         return redirect('store')

#     grand_total = 0
#     tax = 0
#     for cart_item in cart_items:
#         total += cart_item.product.price * cart_item.quantity
#         quantity += cart_item.quantity

#     tax = (2 * total) / 100
#     grand_total = total + tax

#     if request.method == 'POST':
#         form = OrderForm(request.POST)

#         if form.is_valid():
#             data = Order()
#             data.user = current_user
#             data.first_name = form.cleaned_data['first_name']
#             data.last_name = form.cleaned_data['last_name']
#             data.phone = form.cleaned_data['phone']
#             data.email = form.cleaned_data['email']
#             data.shipping_address = form.cleaned_data['shipping_address']
#             data.social_media_link = form.cleaned_data['social_media_link']
#             data.country = form.cleaned_data['country']
#             data.state = form.cleaned_data['state']
#             data.city = form.cleaned_data['city']
#             data.order_note = form.cleaned_data['order_note']
#             data.order_total = grand_total
#             data.tax = tax
#             data.ip = request.META.get('REMOTE_ADDR')
#             data.save()

#             # Generate order number
#             current_date = datetime.date.today().strftime("%Y%m%d")
#             data.order_number = f"{current_date}{data.id}"
#             data.save()

#             # Personal Info (safe)
#             pi_first = request.POST.get('pi_first_name')
#             if pi_first:
#                 pi_birthday = None
#                 raw = request.POST.get('pi_birthday', '').strip()
#                 if raw:
#                     for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
#                         try:
#                             pi_birthday = datetime.datetime.strptime(raw, fmt).date()
#                             break
#                         except ValueError:
#                             pass

#                 PersonalInfo.objects.create(
#                     order=data,
#                     first_name=pi_first,
#                     middle_name=request.POST.get('pi_middle_name', ''),
#                     last_name=request.POST.get('pi_last_name', ''),
#                     gender=request.POST.get('pi_gender', ''),
#                     eye_color=request.POST.get('pi_eye_color', ''),
#                     hair_color=request.POST.get('pi_hair_color', ''),
#                     birthday=pi_birthday,
#                     height=request.POST.get('pi_height', ''),
#                     weight=int(request.POST.get('pi_weight')) if request.POST.get('pi_weight') else None,
#                     street_address=request.POST.get('pi_street_address', ''),
#                     city=request.POST.get('pi_city', ''),
#                     zip_code=request.POST.get('pi_zip_code', ''),
#                 )

#             return redirect('payment_method') + f'?order_number={data.order_number}'

#         # ✅ IMPORTANT: form invalid case
#         return redirect('checkout')

#     return redirect('checkout')

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')


def payment_method(request):
    order_number = request.GET.get('order_number')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=False)
        context = {
            'order': order,
        }
        return render(request, 'orders/payment_method.html', context)
    except Order.DoesNotExist:
        return redirect('home')


def crypto_payment(request):
    order_number = request.GET.get('order_number')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=False)
        context = {
            'order': order,
        }
        return render(request, 'orders/crypto_payment.html', context)
    except Order.DoesNotExist:
        return redirect('home')


def process_payment(request):
    if request.method == 'POST':
        order_number = request.POST.get('order_number')
        payment_method = request.POST.get('payment_method')

        try:
            order = Order.objects.get(order_number=order_number, is_ordered=False)
            current_user = request.user
            cart_items = CartItem.objects.filter(user=current_user)

            # Generate payment ID
            reference = str(uuid.uuid4())

            # Create payment based on method
            payment = Payment(
                user=current_user,
                payment_id=reference,
                payment_method=payment_method,
                amount_paid=order.order_total,
                status='Pending' if payment_method == 'CRYPTO' else 'Completed',
            )

            # Handle crypto payment details
            if payment_method == 'CRYPTO':
                crypto_wallet_url = request.POST.get('crypto_wallet_url')
                crypto_payment_proof = request.FILES.get('crypto_payment_proof')

                if crypto_wallet_url and crypto_payment_proof:
                    payment.crypto_wallet_url = crypto_wallet_url
                    payment.crypto_payment_proof = crypto_payment_proof
                else:
                    return redirect(f'/orders/crypto_payment/?order_number={order_number}')

            payment.save()

            # Mark order as ordered and attach payment
            order.payment = payment
            order.is_ordered = True
            order.save()

            # Move the cart items to Order Product table
            for item in cart_items:
                orderproduct = OrderProduct()
                orderproduct.order_id = order.id
                orderproduct.payment = payment
                orderproduct.user_id = current_user.id
                orderproduct.product_id = item.product_id
                orderproduct.quantity = item.quantity
                orderproduct.product_price = item.product.price
                orderproduct.ordered = True
                orderproduct.save()

                cart_item = CartItem.objects.get(id=item.id)
                product_variation = cart_item.variations.all()
                orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                orderproduct.variations.set(product_variation)
                orderproduct.save()

                # Reduce the quantity of the sold products
                product = Product.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()

            # Clear cart
            CartItem.objects.filter(user=current_user).delete()

            # Create support ticket automatically
            if payment_method == 'DIRECT':
                ticket_subject = f'Payment Assistance Required - Order #{order.order_number}'
                ticket_message = f'Hello Admin,\n\nI have placed an order (Order #{order.order_number}) and selected Direct Payment method. Please assist me with the payment process.\n\nOrder Total: ${order.order_total}\nPayment Method: Direct Payment (Paypal/Venmo/CashApp)\n\nThank you!'
            else:  # CRYPTO
                ticket_subject = f'Crypto Payment Submitted - Order #{order.order_number}'
                ticket_message = f'Hello Admin,\n\nI have submitted my crypto payment details for Order #{order.order_number}.\n\nOrder Total: ${order.order_total}\nWallet URL: {payment.crypto_wallet_url}\n\nPayment proof has been uploaded. Please verify and confirm.\n\nThank you!'

            # Create the ticket
            ticket = Ticket.objects.create(
                user=current_user,
                subject=ticket_subject,
                status='open'
            )

            # Create the initial message
            TicketMessage.objects.create(
                ticket=ticket,
                sender=current_user,
                message=ticket_message
            )

            # Redirect to order complete
            return redirect(f'/orders/order_complete/?order_number={order.order_number}&payment_id={payment.payment_id}')

        except Order.DoesNotExist:
            return redirect('home')
    else:
        return redirect('checkout')
