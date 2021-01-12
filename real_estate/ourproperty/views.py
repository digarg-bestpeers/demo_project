from django.shortcuts import render
from .models import EstateProperty, User
from .forms import PropertyUserForm, EstatePropertyForm,FeatureForm, AddressForm, PhotoForm
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from real_estate.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
# Create your views here.


def public_properties(request, dealer_key):
  properties = EstateProperty.objects.filter(user_request="approved", dealer__username=dealer_key).order_by('-id')
  if request.method == "POST":
    property_user_form = PropertyUserForm(request.POST)
    estate_property_form = EstatePropertyForm(request.POST)
    feature_form = FeatureForm(request.POST)
    address_form = AddressForm(request.POST)
    photo_form = PhotoForm(request.POST, request.FILES)
    dealer_obj = User.objects.get(username = dealer_key)
    if property_user_form.is_valid() and estate_property_form.is_valid() and feature_form.is_valid() and address_form.is_valid() and photo_form.is_valid():
      property_user_obj = property_user_form.save()
      subject = 'Property register with Ourproperty'
      message = 'Thank you for registering property with us'
      recepient = property_user_obj.email
      send_mail(subject,message,EMAIL_HOST_USER,[recepient],fail_silently=False)

      estate_property_form.save(commit=False)
      estate_property_form.instance.property_user = property_user_obj
      estate_property_form.instance.dealer = dealer_obj
      estate_property_obj = estate_property_form.save()

      feature_form.save(commit=False)
      feature_form.instance.estate_property = estate_property_obj
      feature_form.save()

      address_form.save(commit=False)
      address_form.instance.estate_property = estate_property_obj
      address_form.save()

      photo_form.save(commit=False)
      photo_form.instance.estate_property = estate_property_obj
      photo_form.save()
      return HttpResponseRedirect('/real-estate/'+dealer_key+'/payment/')

  else:
    property_user_form = PropertyUserForm()
    estate_property_form = EstatePropertyForm()
    feature_form = FeatureForm()
    address_form = AddressForm()
    photo_form = PhotoForm()

  context = {
      'property_user_form': property_user_form,
      'estate_property_form': estate_property_form,
      'feature_form': feature_form,
      'address_form': address_form,
      'photo_form': photo_form,
      'properties': properties,
      'dealer_key': dealer_key
    }
  return render(request, "ourproperty/properties.html", context)

def payment(request, dealer_key):
  if request.method == 'POST':
      # Recent add property with pending payment
      property_obj = EstateProperty.objects.filter(payment_status=False).order_by('-id')[:1]
      for obj in property_obj:
        obj.payment_status = True
        obj.save()
      return HttpResponseRedirect('/real-estate/'+dealer_key)
  return render(request, 'ourproperty/payment.html')

def login_dealer(request):
  if not request.user.is_authenticated:
    if request.method == "POST":
      form = AuthenticationForm(request=request, data=request.POST)
      if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # Validate database credentials with user provided credentials
        user = authenticate(username=username,password=password)
        if user != None:
          login(request, user)
          return HttpResponseRedirect('/real-estate/')
    else:
      form = AuthenticationForm()
      return render(request, 'ourproperty/home.html', {'form':form})
  else:
    return HttpResponseRedirect('/real-estate/')


def logout_dealer(request):
  logout(request)
  return HttpResponseRedirect('/')

def dealer_property(request):
  if request.user.is_authenticated:
    properties = EstateProperty.objects.filter(dealer=request.user).order_by('-id')
    if request.method == 'POST':
      property_user_form = PropertyUserForm(request.POST)
      estate_property_form = EstatePropertyForm(request.POST)
      feature_form = FeatureForm(request.POST)
      address_form = AddressForm(request.POST)
      photo_form = PhotoForm(request.POST, request.FILES)
      dealer_obj = User.objects.get(username = request.user.username)
      if property_user_form.is_valid() and estate_property_form.is_valid() and feature_form.is_valid() and address_form.is_valid() and photo_form.is_valid():
        property_user_obj = property_user_form.save()

        estate_property_form.save(commit=False)
        estate_property_form.instance.property_user = property_user_obj
        estate_property_form.instance.dealer = dealer_obj
        estate_property_form.instance.payment_status = True
        estate_property_form.instance.user_request = "approved"
        estate_property_obj = estate_property_form.save()

        feature_form.save(commit=False)
        feature_form.instance.estate_property = estate_property_obj
        feature_form.save()

        address_form.save(commit=False)
        address_form.instance.estate_property = estate_property_obj
        address_form.save()

        photo_form.save(commit=False)
        photo_form.instance.estate_property = estate_property_obj
        photo_form.save()

        return HttpResponseRedirect('/real-estate/')
    else:
      property_user_form = PropertyUserForm()
      estate_property_form = EstatePropertyForm()
      feature_form = FeatureForm()
      address_form = AddressForm()
      photo_form = PhotoForm()

    context = {
      'property_user_form': property_user_form,
      'estate_property_form': estate_property_form,
      'feature_form': feature_form,
      'address_form': address_form,
      'photo_form': photo_form,
      'properties':properties
    }
    return render(request, "ourproperty/dealer/properties.html", context)
  else:
    return HttpResponseRedirect('/')

def search_data(request):
  if request.method == "POST":
    search1 = request.POST.get("search1")
    search2 = request.POST.get("search2")
    if request.user.is_authenticated:
      properties = EstateProperty.objects.filter(dealer=request.user, property_address__city__icontains=search1, property_address__address__icontains=search2)
      properties_data_html = render_to_string("ourproperty/dealer/partial/properties.html", context={'properties':properties})
    else:
      dealer_key = request.POST.get("dealer_key")
      properties = EstateProperty.objects.filter(user_request="approved", dealer__username=dealer_key, property_address__city__icontains=search1, property_address__address__icontains=search2)
      properties_data_html = render_to_string("ourproperty/partial/properties.html", context={'properties':properties})
    return JsonResponse({'status':200, 'properties_data_html':properties_data_html})
  else:
    return JsonResponse({'warning': 'Page Not Found'})

def dealer_approval(request):
  if request.method == "GET":
    permit_data = request.GET.get('permit_data')
    permit_data_obj_id = int(request.GET.get('permit_data_obj_id'))
    obj = EstateProperty.objects.get(id=permit_data_obj_id)
    obj.user_request = permit_data
    obj.save()
    properties = EstateProperty.objects.filter(dealer=obj.dealer)
    properties_data_html = render_to_string("ourproperty/dealer/partial/properties.html", context={'properties':properties})
    return JsonResponse({'status':200, 'properties_data_html':properties_data_html})





