from django import forms
from ourproperty.models import *


class PropertyUserForm(forms.ModelForm):
  class Meta:
    model = PropertyUser
    fields = '__all__'
    widgets = {'password': forms.PasswordInput()}

  # def clean_mobile(self):
  #   mobile = str(self.cleaned_data['mobile'])
  #   if len(mobile) != 10:
  #     raise forms.ValidationError("Mobile number should have 10 digits only")
  #   return mobile

class EstatePropertyForm(forms.ModelForm):
  class Meta:
    model = EstateProperty
    exclude = ['property_user', 'payment_status', 'user_request']
    labels = {
      'title': 'Property Title', 'estate_type': 'Property Type'
    }

class FeatureForm(forms.ModelForm):
  class Meta:
    model = Feature
    exclude = ['estate_property']
    labels = {'area': 'Area(sq-ft)'}

class AddressForm(forms.ModelForm):
  class Meta:
    model = Address
    exclude = ['estate_property']

class PhotoForm(forms.ModelForm):
  class Meta:
    model = PropertyPhoto
    exclude = ['estate_property']
