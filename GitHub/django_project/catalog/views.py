from django.contrib import messages
from django.db.models import Q,Count,Avg
from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Item,Category
from .forms import FeedbackForm,ItemForm
TITLE='Каталог літературних подій'
def home(request):
 return render(request,'home.html',{'title':TITLE,'count':Item.objects.count(),'items':list(Item.objects.select_related('category')[:10])})
def items(request):
 query=request.GET.get('q','')
 data=Item.objects.select_related('category').filter(Q(title__icontains=query)|Q(description__icontains=query))
 return render(request,'items.html',{'title':TITLE,'count':data.count(),'items':data})
def item_detail(request,pk):
 return render(request,'detail.html',{'item':get_object_or_404(Item,pk=pk)})
def feedback(request):
 form=FeedbackForm(request.POST or None)
 if request.method=='POST' and form.is_valid():
  messages.success(request,'Повідомлення успішно перевірено та прийнято')
  return redirect('feedback')
 return render(request,'feedback.html',{'form':form})
def create_item(request):
 form=ItemForm(request.POST or None)
 if request.method=='POST' and form.is_valid():
  item=form.save();messages.success(request,'Запис створено');return redirect('item_detail',pk=item.pk)
 return render(request,'edit.html',{'form':form})
def update_item(request,pk):
 item=get_object_or_404(Item,pk=pk);form=ItemForm(request.POST or None,instance=item)
 if request.method=='POST' and form.is_valid():
  form.save();return redirect('item_detail',pk=pk)
 return render(request,'edit.html',{'form':form})
def delete_item(request,pk):
 item=get_object_or_404(Item,pk=pk)
 if request.method=='POST':item.delete();return redirect('items')
 return render(request,'delete.html',{'item':item})
@require_http_methods(['GET','POST'])
def api_items(request):
 if request.method=='GET':
  return JsonResponse({'items':list(Item.objects.values('id','title','price','available'))})
 import json
 try:
  payload=json.loads(request.body);title=str(payload['title']).strip();category=Category.objects.get(pk=payload['category_id'])
  if not title:raise ValueError('Порожня назва')
  item=Item.objects.create(title=title,category=category,price=payload.get('price',0))
  return JsonResponse({'id':item.pk,'title':item.title},status=201)
 except (ValueError,KeyError,TypeError,Category.DoesNotExist) as exc:return JsonResponse({'error':str(exc)},status=400)
@require_http_methods(['GET','PATCH','DELETE'])
def api_item(request,pk):
 item=get_object_or_404(Item,pk=pk)
 if request.method=='GET':return JsonResponse({'id':item.pk,'title':item.title})
 if request.method=='DELETE':item.delete();return JsonResponse({},status=204)
 import json
 try:
  payload=json.loads(request.body);item.title=str(payload['title']).strip()
  if not item.title:raise ValueError('Порожня назва')
  item.save();return JsonResponse({'id':item.pk,'title':item.title})
 except (ValueError,KeyError,TypeError) as exc:return JsonResponse({'error':str(exc)},status=400)
def statistics(request):
 return JsonResponse({'count':Item.objects.count(),'average':Item.objects.aggregate(v=Avg('price'))['v'],'by_category':list(Category.objects.annotate(total=Count('items')).values('name','total'))})
