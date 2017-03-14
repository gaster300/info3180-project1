from . import db

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    age=db.Column(db.Integer)
    gender=db.Column(db.String(6))
    biography=db.Column(db.String(80))
    image=db.Column(db.LargeBinary)
    created_on=db.Column(db.DateTime)
    
    
    def __init__(self, id, username, firstname, lastname, age, biography, sex, image, created_on):
        
            self.id=id
            self.username=username
            self.firstname=firstname.title()
            self.lastname=lastname.title()
            self.age=age
            self.biography=biography
            self.sex = sex.upper()
            self.image=image
            self.created_on=created_on

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
