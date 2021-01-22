from django import forms
from ourproperty.models import *

class EstatePropertyForm(forms.ModelForm):
  class Meta:
    model = EstateProperty
    exclude = ['dealer', 'created_by', 'payment_status', 'user_request']
    labels = {
      'title': 'Property Title', 'estate_type': 'Property Type'
    }

class FeatureForm(forms.ModelForm):
  class Meta:
    model = Feature
    exclude = ['estate_property']
    labels = {
      'area': 'Area(sq-ft)',
      'status': 'Property Status'
      }

class AddressForm(forms.ModelForm):
  class Meta:
    model = Address
    exclude = ['estate_property']

class PhotoForm(forms.ModelForm):
  class Meta:
    model = PropertyPhoto
    fields = ['photo']
    # exclude = ['estate_property']
    widgets = {
              # 'photo': forms.FileInput(attrs={'multiple': True})
              'photo': forms.FileInput()
        }

class UserForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'email']

  # def clean(self):
  #   cleaned_data = super(UserForm, self).clean()
  #   email = cleaned_data.get('email')
  #   if User.objects.filter(email=email).exists():
  #     raise forms.ValidationError('Email already exists')


class UserTypeForm(forms.ModelForm):
  class Meta:
    model = UserType
    fields = ['mobile']

  # def clean_mobile(self):
  #   mobile = str(self.cleaned_data['mobile'])
  #   if len(mobile) != 10:
  #     raise forms.ValidationError("Mobile number should have 10 digits only")
  #   return mobile

class EditUserForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['first_name', 'last_name']
