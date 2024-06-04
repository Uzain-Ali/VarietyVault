from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

STATE_CHOICES = (
    ('Azad Kashmir', 'Azad Kashmir'),
    ('Balochistan', 'Balochistan'),
    ('Gilgit-Baltistan', 'Gilgit-Baltistan'),
    ('Islamabad Capital Territory', 'Islamabad Capital Territory'),
    ('Khyber Pakhtunkhwa', 'Khyber Pakhtunkhwa'),
    ('Punjab', 'Punjab'),
    ('Sindh', 'Sindh'),
)

City_CHOICES = (
    ('Abbottabad', 'Abbottabad'),
    ('Bahawalpur', 'Bahawalpur'),
    ('Bannu', 'Bannu'),
    ('Chiniot', 'Chiniot'),
    ('Dera Ghazi Khan', 'Dera Ghazi Khan'),
    ('Faisalabad', 'Faisalabad'),
    ('Gujranwala', 'Gujranwala'),
    ('Gujrat', 'Gujrat'),
    ('Hyderabad', 'Hyderabad'),
    ('Islamabad', 'Islamabad'),
    ('Jhang', 'Jhang'),
    ('Jhelum', 'Jhelum'),
    ('Karachi', 'Karachi'),
    ('Kasur', 'Kasur'),
    ('Khushab', 'Khushab'),
    ('Lahore', 'Lahore'),
    ('Larkana', 'Larkana'),
    ('Mandi Bahauddin', 'Mandi Bahauddin'),
    ('Mardan', 'Mardan'),
    ('Multan', 'Multan'),
    ('Murree', 'Murree'),
    ('Muzaffarabad', 'Muzaffarabad'),
    ('Nawabshah', 'Nawabshah'),
    ('Peshawar', 'Peshawar'),
    ('Quetta', 'Quetta'),
    ('Rahim Yar Khan', 'Rahim Yar Khan'),
    ('Rawalpindi', 'Rawalpindi'),
    ('Sahiwal', 'Sahiwal'),
    ('Sargodha', 'Sargodha'),
    ('Sheikhupura', 'Sheikhupura'),
    ('Sialkot', 'Sialkot'),
    ('Sukkur', 'Sukkur'),
    ('Swat', 'Swat'),
    ('Vehari', 'Vehari'),
)

CATEGORY_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear'),
)


STATUS_CHOICES=(
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(choices=City_CHOICES,max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=50)

    class Meta:
        db_table="customer"

    def __str__(self):
        return str(self.id)
    




class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=100)
    product_image = models.ImageField(upload_to='productimg')

    class Meta:
        db_table = "product"

    def __str__(self):
        return str(self.id)
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'cart'

    def __str__(self):
        return str(self.id)
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        db_table = "orderplaced"
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price