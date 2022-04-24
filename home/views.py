from django.shortcuts import render
from .models import *
from django.views.generic import View
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