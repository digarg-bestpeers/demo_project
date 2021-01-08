from django.db import models
from django.contrib.auth.models import User
# Create your models here.

STATUS_CHOICES = (('furnished','Furnished'),('semifurnished','Semifurnished'), ('unfurnished','Unfurnished'))



class PropertyUser(models.Model):
    '''Property owner detail'''
    full_name = models.CharField(max_length=100)
    mobile = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.email

class EstateProperty(models.Model):
    '''Property declaration'''
    property_user = models.ForeignKey(PropertyUser, on_delete=models.CASCADE)
    dealer = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="dealer_property")
    title = models.CharField(max_length=30)
    estate_type = models.CharField(max_length=200)
    monthly_charge = models.IntegerField()
    security_charge = models.IntegerField()
    maintainence_charge = models.IntegerField()
    property_posted_date = models.DateField(auto_now_add=True, null=True)
    payment_status = models.BooleanField(default=False)
    user_request = models.CharField(max_length=20, default="pending")


    def __str__(self):
        return self.title


class Address(models.Model):
    '''Property address information'''
    estate_property = models.OneToOneField(EstateProperty, on_delete=models.CASCADE, related_name='property_address')
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=20)
    pincode = models.IntegerField()
    landmark = models.CharField(max_length=100, blank=True)


class Feature(models.Model):
    '''Property feature declaration'''
    estate_property = models.OneToOneField(EstateProperty, on_delete=models.CASCADE, related_name='property_feature')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    bedroom = models.IntegerField()
    bathroom = models.IntegerField()
    balcony = models.IntegerField()
    floor = models.IntegerField()
    area = models.IntegerField()

def get_photo_path(instance, filename):
    instance_id = instance.estate_property.id
    return 'images/{}/{}'.format(instance_id, filename)

class PropertyPhoto(models.Model):
    '''Property photo detail'''
    estate_property = models.ForeignKey(EstateProperty, on_delete=models.CASCADE, related_name='property_photos')
    photo = models.ImageField(upload_to=get_photo_path, max_length=255)
    photo_create = models.DateField(auto_now_add = True)
    photo_update = models.DateField(auto_now = True)

