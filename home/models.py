from django.db import models

# Create your models here.

LABELS = (('hot','hot'),('new','new'),('sale','sale'),('','default'))

class Category(models.Model):
	name = models.CharField(max_length = 400)
	image = models.ImageField(upload_to = 'media')
	slug = models.CharField(max_length = 500,unique = True)

	def __str__(self):
		return self.name

class SubCategory(models.Model):
	name = models.CharField(max_length = 400)
	category = models.ForeignKey(Category,on_delete = models.CASCADE)
	image = models.ImageField(upload_to = 'media')
	slug = models.CharField(max_length = 500,unique = True)

	def __str__(self):
		return self.name

class Slider(models.Model):
	name = models.CharField(max_length = 400)
	image = models.ImageField(upload_to = 'media')
	title = models.TextField()
	rank = models.IntegerField(default = 1)
	status = models.CharField(choices = (('active','active'),('','default')),max_length = 25,blank = True)
	description = models.TextField(blank = True)

	def __str__(self):
		return self.name

class Ad(models.Model):
	name = models.CharField(max_length = 400)
	image = models.ImageField(upload_to = 'media')
	title = models.TextField()
	rank = models.IntegerField(default = 1)

	def __str__(self):
		return self.name

class Contact(models.Model):
	name = models.CharField(max_length = 300)
	email = models.EmailField(max_length = 300,blank = True)
	phone = models.CharField(blank = True,max_length = 200)
	subject = models.TextField()
	message = models.TextField()

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length = 400)
	image = models.ImageField(upload_to = 'media')
	price = models.IntegerField()
	discounted_price = models.IntegerField()
	category = models.ForeignKey(Category,on_delete = models.CASCADE)
	subcategory = models.ForeignKey(SubCategory,on_delete = models.CASCADE)
	status = models.CharField(max_length = 50,choices = (('active','active'),('inactive','inactive')))
	labels = models.CharField(max_length = 50,choices = LABELS)

	def __str__(self):
		return self.name


