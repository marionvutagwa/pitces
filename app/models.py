from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index =True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))

    #relation
    pitches = db.relationship('Pitch',backref = 'user',lazy = "dynamic")
    comment = db.relationship('Comment',backref = 'user',lazy = "dynamic") 
    upvote = db.relationship('UpVote',backref = 'user',lazy = "dynamic") 
    downvote = db.relationship('DownVote',backref = 'user',lazy = "dynamic") 
    

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
            return check_password_hash(self.password_hash,password)    


    def __repr__(self):
        return f'User {self.username}'


class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")
    

    def __repr__(self):
        return f'User {self.name}'

class Pitch(db.Model):

    __tablename__ = 'pitches'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    category = db.Column(db.String)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    time = db.Column(db.DateTime,default=datetime.utcnow)
    comments = db.relationship('Comment',backref='pitch',lazy='dynamic')
    upvote = db.relationship('UpVote',backref='pitch',lazy='dynamic')
    downvote = db.relationship('DownVote',backref='pitch',lazy='dynamic')


    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitch(cls,category):
        pitches = Pitch.query.filter_by(category=category).all()
        return pitches  
          
    # def __repr__(self):
    #     return f"Pitch ('{self.id}','{self.time}')"   


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    description = db.Column(db.String)   
    pitch_id = db.Column(db.Integer,db.ForeignKey("pitches.id"),nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable = False)
   
    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,pitch_id):
        comments = Comment.query.filter_by(pitch_id = pitch_id).all()
        return comments
    
    def __repr__(self):
        return f'comment: {self.comment}'

class UpVote(db.Model):
    __tablename__ = 'upvotes'        
    id = db.Column(db.Integer,primary_key = True)
    pitch_id = db.Column(db.Integer,db.ForeignKey("pitches.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    upvote = db.Column(db.Integer, default= 1)


    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_upvotes(cls,pitch_id):
        upvote = UpVote.query.filter_by(pitch_id = pitch_id).all()
        return upvote 
    
    def __repr__(self):
        return f'User {self.pitch_id},{self.user_id}'


class DownVote(db.Model):
    __tablename__ = 'downvotes'

    id = db.Column(db.Integer,primary_key = True)
    pitch_id = db.Column(db.Integer,db.ForeignKey("pitches.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    downvote = db.Column(db.Integer, default= 1)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_downvotes(cls,pitch_id):
        downvote = DownVote.query.filter_by(pitch_id = pitch_id).all()
        return upvote    

    def __repr__(self):
        return f'User {self.pitch_id},{self.user_id}'    