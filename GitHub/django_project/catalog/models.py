from django.db import models
from django.urls import reverse
class Category(models.Model):
 name=models.CharField(max_length=90,unique=True)
 description=models.TextField(blank=True)
 code=models.SlugField(unique=True)
 class Meta:
  ordering=['name'];verbose_name='Категорія';verbose_name_plural='Категорії'
 def __str__(self):return self.name
class Tag(models.Model):
 name=models.CharField(max_length=80,unique=True)
 slug=models.SlugField(unique=True)
 description=models.CharField(max_length=150,blank=True)
 class Meta:
  ordering=['name'];verbose_name='Мітка';verbose_name_plural='Мітки'
 def __str__(self):return self.name
class Item(models.Model):
 title=models.CharField(max_length=150)
 category=models.ForeignKey(Category,on_delete=models.PROTECT,related_name='items')
 tags=models.ManyToManyField(Tag,blank=True,related_name='items')
 price=models.DecimalField(max_digits=9,decimal_places=2,default=0)
 description=models.TextField(blank=True)
 available=models.BooleanField(default=True)
 class Meta:
  ordering=['title'];verbose_name='Позиція';verbose_name_plural='Позиції'
 def __str__(self):return self.title
 def get_absolute_url(self):return reverse('item_detail',args=[self.pk])
class ItemDetail(models.Model):
 item=models.OneToOneField(Item,on_delete=models.CASCADE,related_name='detail')
 identifier=models.CharField(max_length=50,unique=True)
 notes=models.TextField(blank=True)
 updated_at=models.DateTimeField(auto_now=True)
 class Meta:
  ordering=['identifier'];verbose_name='Деталі';verbose_name_plural='Деталі'
 def __str__(self):return self.identifier
