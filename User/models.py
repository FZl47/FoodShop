from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import Sum, F
from Food.models import Meal, NotifyMe
from Config import tools
from Config import task
from Config.tools import static_url, domain_url


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=70, null=True, default='Unknown')
    last_name = models.CharField(max_length=70, null=True, default='Unknown')
    phone_number = models.CharField(max_length=15, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_image(self):
        return static_url('images/image-default-user.png')

    def __str__(self):
        return self.get_name()

    def add_to_cart(self, slug, count=1):
        count = str(count)
        if count.isdigit():
            count = int(count)
        else:
            count = 1
        meal = Meal.get_objects.get_by_slug(slug)
        if meal:
            if meal.is_available():
                order = self.get_order_active()
                orderDetails = order.get_details()
                orderDetail = orderDetails.filter(meal=meal).first()
                if orderDetail:
                    old_count = orderDetail.count
                    new_count = old_count + count
                    if new_count <= meal.stock:
                        orderDetail.count = new_count
                    else:
                        orderDetail.count = meal.stock
                    orderDetail.save()
                else:
                    OrderDetail.objects.create(order=order, meal=meal, count=count)
                return True
        return False

    def get_order_active(self):
        order = self.order_set.filter(is_paid=False).first()
        if order == None:
            order = Order.objects.create(user=self)
        return order

    def get_orders(self):
        orders = self.order_set.filter(is_paid=True).order_by('-id')
        return orders

    def in_my_notify(self, meal):
        notify = self.get_notify(meal)
        return True if notify != None else False

    def get_notify(self, meal):
        return self.notifyme_set.filter(meal=meal).first()

    def get_notifications(self):
        return self.notifyme_set.all()

    def get_address(self):
        return self.address_set.all()

    def get_comments(self):
        return self.comment_set.all()

    def get_visits(self):
        # data = tools.Distinct(self.visitmeal_set.model,self.visitmeal_set.all().order_by('id'),'meal')
        data = self.visitmeal_set.all().order_by('-time_visit')
        return data



class Order(models.Model):

    STATUS_ORDER = (
        ('nothing','Nothing'),
        ('preparation','Preparation'),
        ('sending','Sending'),
        ('delivered','ِelivered'),
    )

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    time_pay = models.DateTimeField(null=True, blank=True)
    price_paid = models.PositiveIntegerField(null=True, blank=True)
    address = models.ForeignKey('Address',on_delete=models.SET_NULL,null=True)
    status_order = models.CharField(max_length=20,choices=STATUS_ORDER,default=STATUS_ORDER[0][0])
    detail = models.TextField(null=True,blank=True)

    def __str__(self):
        return f"Order - {self.user.get_name()}"

    def get_details(self):
        return self.orderdetail_set.all()

    def get_price_meals(self):
        orderdetails = self.get_details()
        return tools.get_decimal_num(
            sum([float(orderdetail.meal.get_price()) * orderdetail.count for orderdetail in orderdetails]))

    def get_price_meals_without_discount(self):
        return tools.get_decimal_num(self.get_details().annotate(total=F('count') * F('meal__price')).aggregate(price=Sum('total'))['price'] or 0)

    def clear_order(self):
        self.get_details().delete()

    def order_is_not_empty(self):
        return True if self.get_details().count() > 0 else False

    def is_available(self):
        return all(self.get_details())

    def get_time_past(self):
        return tools.GetDifferenceTime(self.time_pay)



class OrderDetail(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    meal = models.ForeignKey('Food.Meal', on_delete=models.SET_NULL, null=True, blank=True)
    count = models.IntegerField(default=1)
    detail = models.TextField(null=True)

    def __str__(self):
        return f'OrderDetail - {tools.TextToShortText(self.meal.title, 30)}'

    def get_meal(self):
        try:
            return Meal.get_objects.get_subclass(id=self.meal.id)
        except:
            return None

    def get_price(self):
        meal = self.meal
        count = int(self.count)
        price_meal = tools.get_decimal_num(float(meal.get_price()) * count)
        return price_meal

    def is_available(self):
        return True if self.meal.stock >= self.count else False

    def payment_orderdetail(self):
        self.detail = f"""
            title : {self.meal.title} - 
            slug  : {domain_url(self.meal.slug)} - 
            count : {self.count}X - 
            Total : {self.get_price()}                
        """

        self.meal.stock -= self.count
        self.meal.save()
        self.save()


class Address(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    address = models.TextField()
    postal_code = models.CharField(max_length=20)
    location = models.CharField(max_length=30, null=True, blank=True)
    cost = models.DecimalField(decimal_places=2, max_digits=8)

    def __str__(self):
        return tools.TextToShortText(self.address, 40)

    def is_free(self):
        return True if self.cost == 0 else False
