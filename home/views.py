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

class CategoryView(BaseView):
	def get(self,request,slug):
		cat_id = Category.objects.get(slug = slug).id
		cat_name = Category.objects.get(slug = slug).name

		self.view['Cat_products'] = Product.objects.filter(category_id = cat_id)
		self.view['Category_name'] = cat_name
		return render(request,'category.html',self.view)


class SubCategoryView(BaseView):
	def get(self,request,slug):
		subcat_id = SubCategory.objects.get(slug = slug).id
		subcat_name = SubCategory.objects.get(slug = slug).name

		self.view['subCat_products'] = Product.objects.filter(subcategory_id = subcat_id)
		self.view['subCategory_name'] = subcat_name
		return render(request,'subcategory.html',self.view)