from django.db import models
from accounts.models import Account
from store.models import Product, Variation



class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('DIRECT', 'Direct Payment'),
        ('CRYPTO', 'Crypto Payment'),
        ('REF', 'Reference'),
    )

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES, default='DIRECT')
    amount_paid = models.CharField(max_length=100) # this is the total amount paid
    status = models.CharField(max_length=100)
    crypto_wallet_url = models.CharField(max_length=500, blank=True, null=True)
    crypto_payment_proof = models.ImageField(upload_to='payment_proofs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Payment, self).save(*args, **kwargs)

        # Auto-update related order status when payment is verified
        if self.status == 'Completed':
            # Get all orders with this payment
            orders = Order.objects.filter(payment=self)
            for order in orders:
                # If order is still in 'New' status, move it to 'Accepted'
                if order.status == 'New':
                    order.status = 'Accepted'
                    # Use update to avoid triggering the Order.save() method again
                    Order.objects.filter(id=order.id).update(status='Accepted')

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    shipping_address = models.CharField(max_length=50)
    social_media_link = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.shipping_address}'

    def save(self, *args, **kwargs):
        # Auto-sync payment status when order status changes
        if self.payment:
            # If order is completed or accepted, mark payment as completed
            if self.status in ['Completed', 'Accepted']:
                self.payment.status = 'Completed'
                self.payment.save()
            # If order is cancelled, mark payment accordingly
            elif self.status == 'Cancelled':
                self.payment.status = 'Cancelled'
                self.payment.save()

        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name


class PersonalInfo(models.Model):
    GENDER_CHOICES = (
        ('M','Male'),
        ('F','Female'),
        ('O','Other'),
    )

    order = models.OneToOneField('Order', on_delete=models.CASCADE, related_name='personal_info', null=True, blank=True)
    first_name = models.CharField(max_length=80)
    middle_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    eye_color = models.CharField(max_length=30, blank=True)
    hair_color = models.CharField(max_length=30, blank=True)
    birthday = models.DateField(null=True, blank=True)
    height = models.CharField(max_length=50, blank=True, help_text='e.g., 5\'8" or 173 cm')
    weight = models.PositiveIntegerField(null=True, blank=True, help_text='Weight in lbs')
    photo = models.ImageField(upload_to='personal_info_photos/', blank=True, null=True)
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'PersonalInfo for order {self.order_id or "unassigned"} - {self.first_name} {self.last_name}'
