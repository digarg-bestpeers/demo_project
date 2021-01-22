from django.shortcuts import render, redirect
from .models import EstateProperty, User, UserType, PropertyPhoto
from .forms import UserForm, UserTypeForm, EstatePropertyForm,FeatureForm, AddressForm, PhotoForm, EditUserForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from real_estate.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

def send_email(recepient_email_id):
  subject = 'Property register with Ourproperty'
  template = render_to_string("ourproperty/email_template.html")
  send_mail(subject,template,EMAIL_HOST_USER,[recepient_email_id],fail_silently=False)
  return None


def public_properties(request, dealer_key):
  properties = EstateProperty.objects.filter(user_request="approved", dealer__user__username=dealer_key).order_by('-id')
  qs = EstateProperty.objects.filter(user_request="approved", dealer__user__username=dealer_key).distinct('property_address__city')
  if request.method == "POST":
    user_form = UserForm(request.POST)
    user_type_form = UserTypeForm(request.POST)
    estate_property_form = EstatePropertyForm(request.POST)
    feature_form = FeatureForm(request.POST)
    address_form = AddressForm(request.POST)
    photo_form = PhotoForm(request.POST, request.FILES)
    images = request.FILES.getlist('photo')
    # import pdb; pdb.set_trace(  )
    dealer_obj = UserType.objects.get(user__username=dealer_key)
    if user_form.is_valid() and user_type_form.is_valid() and estate_property_form.is_valid() and feature_form.is_valid() and address_form.is_valid() and photo_form.is_valid():
      email = user_form.cleaned_data['email']
      if User.objects.filter(email=email).exists():
        user_obj = User.objects.get(email=email)
      else:
        user_form.instance.username = email
        user_obj = user_form.save()
        password = User.objects.make_random_password()
        print(password)
        user_obj.set_password(password)
        user_obj.save()

        user_type_form.save(commit=False)
        user_type_form.instance.user = user_obj
        user_type_obj = user_type_form.save()

      estate_property_form.save(commit=False)
      estate_property_form.instance.dealer = dealer_obj
      estate_property_form.instance.created_by = user_obj
      estate_property_obj = estate_property_form.save()

      feature_form.save(commit=False)
      feature_form.instance.estate_property = estate_property_obj
      feature_form.save()

      address_form.save(commit=False)
      address_form.instance.estate_property = estate_property_obj
      address_form.save()

      for image in images:
        PropertyPhoto.objects.create(estate_property=estate_property_obj, photo=image)
      # photo_form.save(commit=False)
      # photo_form.instance.estate_property = estate_property_obj
      # photo_form.save()
      return HttpResponseRedirect('/real-estate/'+dealer_key+'/payment/')

  else:
    user_form = UserForm()
    user_type_form = UserTypeForm()
    estate_property_form = EstatePropertyForm()
    feature_form = FeatureForm()
    address_form = AddressForm()
    photo_form = PhotoForm()

  context = {
      'user_form': user_form,
      'user_type_form': user_type_form,
      'estate_property_form': estate_property_form,
      'feature_form': feature_form,
      'address_form': address_form,
      'photo_form': photo_form,
      'properties': properties,
      'dealer_key': dealer_key,
      'qs': qs
    }
  return render(request, "ourproperty/properties.html", context)

def payment(request, dealer_key):
  if request.method == 'POST':
      # Recent add property with pending payment
      property_obj = EstateProperty.objects.filter(payment_status=False).order_by('-id')[:1]
      for obj in property_obj:
        obj.payment_status = True
        obj.save()
        recepient_email_id = obj.created_by.username
        send_email(recepient_email_id)
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
          if(user.user_type.user_roll == 'dealer'):
            return HttpResponseRedirect('/real-estate/')
          else:
            return HttpResponseRedirect('/dashboard/')
    else:
      form = AuthenticationForm()
      return render(request, 'ourproperty/home.html', {'form':form})
  else:
    if (request.user.user_type.user_roll == 'dealer'):
      return HttpResponseRedirect('/real-estate/')
    else:
      return HttpResponseRedirect('/dashboard/')


def logout_dealer(request):
  logout(request)
  return HttpResponseRedirect('/')

def dealer_property(request):
  if request.user.is_authenticated:
    properties = EstateProperty.objects.filter(dealer__user__username=request.user).order_by('-id')
    qs = EstateProperty.objects.filter(dealer__user__username=request.user).distinct('property_address__city')
    if request.method == 'POST':
      user_form = UserForm(request.POST)
      user_type_form = UserTypeForm(request.POST)
      estate_property_form = EstatePropertyForm(request.POST)
      feature_form = FeatureForm(request.POST)
      address_form = AddressForm(request.POST)
      photo_form = PhotoForm(request.POST, request.FILES)
      dealer_obj = UserType.objects.get(user__username=request.user)
      if user_form.is_valid() and user_type_form.is_valid() and estate_property_form.is_valid() and feature_form.is_valid() and address_form.is_valid() and photo_form.is_valid():
        email = user_form.cleaned_data['email']
        if User.objects.filter(email=email).exists():
          user_obj = User.objects.get(email=email)
        else:
          user_form.instance.username = email
          user_obj = user_form.save()
          password = User.objects.make_random_password()
          print(password)
          user_obj.set_password(password)
          user_obj.save()

          user_type_form.save(contextommit=False)
          user_type_form.instance.user = user_obj
          user_type_obj = user_type_form.save()

        estate_property_form.save(commit=False)
        estate_property_form.instance.dealer = dealer_obj
        estate_property_form.instance.created_by = user_obj
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

        recepient_email_id = email
        send_email(recepient_email_id)
        return HttpResponseRedirect('/real-estate/')
    else:
      user_form = UserForm()
      user_type_form = UserTypeForm()
      estate_property_form = EstatePropertyForm()
      feature_form = FeatureForm()
      address_form = AddressForm()
      photo_form = PhotoForm()

    context = {
      'user_form': user_form,
      'user_type_form': user_type_form,
      'estate_property_form': estate_property_form,
      'feature_form': feature_form,
      'address_form': address_form,
      'photo_form': photo_form,
      'properties':properties,
      'qs': qs,
    }
    return render(request, "ourproperty/dealer/properties.html", context)
  else:
    return HttpResponseRedirect('/')

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

def search(request):
  if request.method == "GET":
    title = request.GET.get("title")
    city = request.GET.get("city")
    status = request.GET.get("status")
    if request.user.is_authenticated:
      if(title==None and city==None and status==None):
        properties = EstateProperty.objects.filter(dealer__user__username=request.user.username)
      else:
        properties = EstateProperty.objects.filter(dealer__user__username=request.user.username, title__icontains=title, property_address__city__icontains=city, property_feature__status__istartswith=status)
      properties_data_html = render_to_string("ourproperty/dealer/partial/properties.html", context={'properties':properties})
    else:
      dealer_key = request.GET.get("dealer_key")
      if(title==None and city==None and status==None):
        properties = EstateProperty.objects.filter(user_request="approved", dealer__user__username=dealer_key)
      else:
        properties = EstateProperty.objects.filter(user_request="approved", dealer__user__username=dealer_key, title__icontains=title, property_address__city__icontains=city, property_feature__status__istartswith=status)
      properties_data_html = render_to_string("ourproperty/partial/properties.html", context={'properties':properties})
    return JsonResponse({'status':200, 'properties_data_html':properties_data_html})


@method_decorator(login_required, name='dispatch')
class EndUser(ListView):
  model = EstateProperty
  template_name = 'ourproperty/enduser/index.html'

  def get_queryset(self):
    qs = super(EndUser, self).get_queryset()
    qs=qs.filter(created_by__username=self.request.user.username)
    return qs

def property_update(request, pk):
  if request.user.is_authenticated:
    obj = EstateProperty.objects.get(id=pk)
    if request.method == 'POST':
      user_form = EditUserForm(request.POST,instance=obj.created_by)
      user_type_form = UserTypeForm(request.POST,instance=obj.created_by.user_type)
      estate_property_form = EstatePropertyForm(request.POST,instance=obj)
      feature_form = FeatureForm(request.POST,instance=obj.property_feature)
      address_form = AddressForm(request.POST,instance=obj.property_address)
      photo_form = PhotoForm(request.POST, request.FILES, instance=obj.property_photos.get())

      if user_form.is_valid() and user_type_form.is_valid() and estate_property_form.is_valid() and feature_form.is_valid() and address_form.is_valid() and photo_form.is_valid():
        user_form.save()
        user_type_form.save()
        estate_property_form.save(commit=False)
        if(request.user.user_type.user_roll=='dealer'):estate_property_form.instance.user_request = 'approved'
        else:
          estate_property_form.instance.user_request = 'pending'
        estate_property_form.save()
        feature_form.save()
        address_form.save()
        photo_form.save()
        return HttpResponseRedirect('/real-estate/update/'+str(pk)+'/')

    else:
      user_form = EditUserForm(instance=obj.created_by)
      user_type_form = UserTypeForm(instance=obj.created_by.user_type)
      estate_property_form = EstatePropertyForm(instance=obj)
      feature_form = FeatureForm(instance=obj.property_feature)
      address_form = AddressForm(instance=obj.property_address)
      photo_form = PhotoForm(instance=obj.property_photos.get())
      context = {
        'user_form': user_form,
        'user_type_form': user_type_form,
        'estate_property_form': estate_property_form,
        'feature_form': feature_form,
        'address_form': address_form,
        'photo_form': photo_form, 'obj':obj
      }
      return render(request, 'ourproperty/enduser/edit.html', context)
  else:
    return HttpResponseRedirect('/')



