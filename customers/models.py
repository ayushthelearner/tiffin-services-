from django.db import models

# Create your models here.
class Customer(models.Model):
    Full_Name = models.CharField(max_length=200)
    Address = models.CharField(max_length=400)
    CHOICES=[('Work','Work'),
         ('Home','Home'),('Other','Other')]
    Address_Type = models.CharField(max_length=20,choices=CHOICES, default = 'Work')
    Phone = models.CharField(max_length=10)
    Email = models.EmailField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)  
    Plan_Type = models.CharField(max_length=200,null=True,blank=True)
    # Feedback = models.CharField(max_length=600, null=True,blank=True)

    def __str__(self):
        return self.Full_Name
    

# models.py
from django.db import models

class order(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Assuming orders belong to a user
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')  # e.g., 'pending', 'completed', 'canceled'
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_id} - {self.status}"

