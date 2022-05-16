from django.shortcuts import render,redirect
from .models import *
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.

class BaseView(View):
	view = {}
	view['categories'] = Category.objects.all()


class HomeView(BaseView):
	def get(self,request):
		self.view['categories'] = Category.objects.all()
		self.view['subcategories'] = SubCategory.objects.all()
		self.view['sliders'] = Slider.objects.all()
		self.view['ads'] = Ad.objects.all()
		self.view['products'] = Product.objects.filter(status = 'active')
		self.view['hots'] = Product.objects.filter(labels = 'hot', status = 'active')
		self.view['sales'] = Product.objects.filter(labels = 'sale', status = 'active')
		self.view['news'] = Product.objects.filter(labels = 'new', status = 'active')

		return render(request,'shop-index.html',self.view)

class ProductDetailView(BaseView):
	def get(self,request,slug):
		self.view['product_detail'] = Product.objects.filter(slug = slug)
		return render(request,'shop-item.html',self.view)

class CategoryView(BaseView):
	def get(self,request,slug):
		cat_id = Category.objects.get(slug = slug).id
		cat_name = Category.objects.get(slug = slug).name

		self.view['Cat_products'] = Product.objects.filter(category_id = cat_id)
		self.view['subcats'] = SubCategory.objects.filter(category_id = cat_id)
		self.view['Category_name'] = cat_name
		return render(request,'category.html',self.view)


class SubCategoryView(BaseView):
	def get(self,request,slug):
		subcat_id = SubCategory.objects.get(slug = slug).id
		subcat_name = SubCategory.objects.get(slug = slug).name
		cat_id = SubCategory.objects.get(slug = slug).category_id

		self.view['subCategory'] = SubCategory.objects.filter(category_id = cat_id)
		self.view['subCat_products'] = Product.objects.filter(subcategory_id = subcat_id)
		self.view['subCategory_name'] = subcat_name
		return render(request,'subcategory.html',self.view)

class SearchView(BaseView):
	def get(self,request):
		if request.method == 'GET':
			query = request.GET['query']
			self.view['search_query'] = query
			self.view['search_product'] = Product.objects.filter(name__icontains = query)

		return render(request,'shop-search-result.html',self.view)

def signup(request):
	if request.method == "POST":
		first_name = request.POST['fname']
		last_name = request.POST['lname']
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		cpassword = request.POST['cpassword']
		if password == cpassword:
			if User.objects.filter(username = username).exists():
				messages.error(request,'The username is already used')
				return render(request,'shop-standart-forms.html')

			elif User.objects.filter(email = email).exists():
				
				messages.error(request,'The email is already used')
				return render(request,'shop-standart-forms.html')
			else:
				user = User.objects.create_user(
					first_name = first_name,
					last_name = last_name,
					username = username,
					email = email,
					password = password
					)
				user.save()
		else:
			messages.error(request,'The password does not match')
			return render(request,'shop-standart-forms.html')
	return render(request,'shop-standart-forms.html')

class CartView(BaseView):
	def get(self,request):
		self.view['cart_product'] = Cart.objects.filter(user = request.user.username,checkout = False)
		return render(request,'shop-shopping-cart.html',self.view)


 
def add_to_cart(request,slug):
	if Cart.objects.filter(slug = slug,user = request.user.username,checkout = False).exists():
		quantity = Cart.objects.get(slug = slug,user = request.user.username,checkout = False).quantity
		quantity = quantity +1
		Cart.objects.filter(slug = slug,user = request.user.username,checkout = False).update(quantity = quantity)
	else:
		username = request.user.username
		data = Cart.objects.create(
			user = username,
			slug = slug,
			items = Product.objects.filter(slug = slug)[0]
			)
		data.save()

	return redirect('/mycart')

def deletecart(request,slug):
	if Cart.objects.filter(slug = slug,user = request.user.username,checkout = False).exists():
		Cart.objects.filter(slug = slug,user = request.user.username,checkout = False).delete()

	return redirect('/mycart')

def reducecart(request,slug):
	if Cart.objects.filter(slug = slug,user = request.user.username,checkout = False).exists():
		quantity = Cart.objects.get(slug = slug,user = request.user.username,checkout = False).quantity
		if quantity > 1:
			quantity = quantity-1
			Cart.objects.filter(slug = slug,user = request.user.username,checkout = False).update(quantity = quantity)

	return redirect('/mycart')

my_email = ''
from django.core.mail import EmailMessage

def contact(request):
	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		message = request.POST['message']
		data = Contact.objects.create(
			name = name,
			email = email,
			message = message
			)
		data.save()

		send_email = EmailMessage(
			'Thank you',
			f'Thank you for messaging us dear {name}',
			my_email,
			[email]
			)
		send_email.send()

	return render(request,'shop-contact.html')
# ---------------------------------------API----------------------------------
from .models import *
from .serializers import *
from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter, SearchFilter

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# ViewSets define the view behavior.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductFilterView(generics.ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer

	filter_backends = (DjangoFilterBackend,OrderingFilter,SearchFilter)
	filter_fields = ['id','category','subcategory','labels','status']
	ordering_fields = ['id','price','name']
	search_fields = ['name','description']


class ProductCRUDViewSet(APIView):
	def get_object(self,pk):
		try:
			return Product.objects.get(pk = pk)
		except:
			print("This id is not in db")

	def get(self,request,pk):
		product = self.get_object(pk)
		serializer = ProductSerializer(product)
		return Response(serializer.data)

	def post(self,request,pk):
		serializer = ProductSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data,status = status.HTTP_201_CREATED)
		return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

	def put(self,request,pk):
		serializer = ProductSerializer(product,data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.data,status = status.HTTP_400_BAD_REQUEST)

	def delete(self,request,pk):
		product.delete()
		return Response(status = status.HTTP_204_NO_CONTENT)



