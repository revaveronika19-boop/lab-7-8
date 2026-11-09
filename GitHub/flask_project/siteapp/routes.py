from flask import Blueprint,render_template,request,redirect,url_for,flash,jsonify,session,make_response,abort,current_app
from sqlalchemy import or_,func
from . import db
from .models import Item,Category
from .forms import FeedbackForm
bp=Blueprint('main',__name__)
@bp.get('/')
def home():
 items=Item.query.limit(10).all()
 return render_template('home.html',title=current_app.config['THEME'],items=items,count=Item.query.count())
@bp.get('/items')
def items():
 q=request.args.get('q','');data=Item.query.filter(or_(Item.title.ilike(f'%{q}%'),Item.description.ilike(f'%{q}%'))).all()
 return render_template('items.html',title=current_app.config['THEME'],items=data,count=len(data))
@bp.route('/feedback',methods=['GET','POST'])
def feedback():
 form=FeedbackForm()
 if form.validate_on_submit():flash('Повідомлення прийнято','success');return redirect(url_for('main.feedback'))
 return render_template('feedback.html',form=form)
@bp.get('/preferences/<theme>')
def preferences(theme):
 if theme not in ('light','dark'):abort(400)
 response=make_response(redirect(url_for('main.home')));response.set_cookie('theme',theme,max_age=86400,samesite='Lax');return response
@bp.post('/cart/<int:item_id>')
def add_to_cart(item_id):
 if not db.session.get(Item,item_id):abort(404)
 cart=session.get('cart',[]);cart.append(item_id);session['cart']=cart
 return jsonify({'cart':cart})
@bp.get('/cart')
def cart():return jsonify({'cart':session.get('cart',[]),'theme':request.cookies.get('theme','light')})
@bp.get('/api/items')
def api_items():
 q=request.args.get('q','');data=Item.query.filter(Item.title.ilike(f'%{q}%')).all()
 return jsonify({'items':[{'id':x.id,'title':x.title,'price':x.price} for x in data]})
@bp.post('/api/items')
def create_item():
 data=request.get_json(silent=True) or {}
 title=str(data.get('title','')).strip()
 if not title:return jsonify({'error':'Порожня назва'}),400
 category=db.session.get(Category,data.get('category_id'))
 if category is None:return jsonify({'error':'Категорію не знайдено'}),400
 try:
  item=Item(title=title,price=float(data.get('price',0)),category=category)
  db.session.add(item);db.session.commit()
  return jsonify({'id':item.id,'title':item.title}),201
 except (ValueError,TypeError):db.session.rollback();return jsonify({'error':'Некоректна ціна'}),400
@bp.route('/api/items/<int:pk>',methods=['GET','PUT','PATCH','DELETE'])
def api_item(pk):
 item=db.session.get(Item,pk)
 if item is None:return jsonify({'error':'Не знайдено'}),404
 if request.method=='GET':return jsonify({'id':item.id,'title':item.title,'price':item.price})
 if request.method=='DELETE':db.session.delete(item);db.session.commit();return '',204
 data=request.get_json(silent=True) or {}
 if request.method=='PUT' and 'title' not in data:return jsonify({'error':'Потрібна назва'}),400
 if 'title' in data:
  if not str(data['title']).strip():return jsonify({'error':'Порожня назва'}),400
  item.title=str(data['title']).strip()
 if 'price' in data:
  try:item.price=float(data['price'])
  except (ValueError,TypeError):db.session.rollback();return jsonify({'error':'Некоректна ціна'}),400
 db.session.commit();return jsonify({'id':item.id,'title':item.title})
@bp.get('/api/stats')
def stats():
 return jsonify({'count':Item.query.count(),'average_price':db.session.query(func.avg(Item.price)).scalar()})
