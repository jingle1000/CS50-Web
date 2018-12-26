class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(15), unique=True)
    email = db.Column('email', db.String(50), unique=True)
    password = db.Column('passwork', db.String(80))
