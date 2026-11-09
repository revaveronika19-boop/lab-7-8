from . import db
item_tags=db.Table('item_tags',db.Column('item_id',db.Integer,db.ForeignKey('item.id'),primary_key=True),db.Column('tag_id',db.Integer,db.ForeignKey('tag.id'),primary_key=True))
class Category(db.Model):
 id=db.Column(db.Integer,primary_key=True)
 name=db.Column(db.String(90),nullable=False,unique=True)
 code=db.Column(db.String(50),nullable=False,unique=True)
 description=db.Column(db.Text,default='')
 items=db.relationship('Item',back_populates='category')
 def __str__(self):return self.name
class Tag(db.Model):
 id=db.Column(db.Integer,primary_key=True)
 name=db.Column(db.String(80),unique=True,nullable=False)
 slug=db.Column(db.String(80),unique=True,nullable=False)
 description=db.Column(db.String(150),default='')
class Item(db.Model):
 id=db.Column(db.Integer,primary_key=True)
 title=db.Column(db.String(150),nullable=False)
 price=db.Column(db.Float,default=0)
 description=db.Column(db.Text,default='')
 available=db.Column(db.Boolean,default=True)
 category_id=db.Column(db.Integer,db.ForeignKey('category.id'),nullable=False)
 category=db.relationship('Category',back_populates='items')
 tags=db.relationship('Tag',secondary=item_tags,backref='items')
 detail=db.relationship('ItemDetail',back_populates='item',uselist=False,cascade='all,delete-orphan')
 def __str__(self):return self.title
class ItemDetail(db.Model):
 id=db.Column(db.Integer,primary_key=True)
 item_id=db.Column(db.Integer,db.ForeignKey('item.id'),unique=True,nullable=False)
 identifier=db.Column(db.String(50),unique=True,nullable=False)
 notes=db.Column(db.Text,default='')
 item=db.relationship('Item',back_populates='detail')
