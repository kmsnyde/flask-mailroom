import os
#import base64

from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256
from model import Donor, Donation, User

app = Flask(__name__)
#use below for local
#app.secret_key = b'\x9d\xb1u\x08%\xe0\xd0p\x9bEL\xf8JC\xa3\xf4J(hAh\xa4\xcdw\x12S*,u\xec\xb8\xb8'
#use below for ??
#app.secret_key = os.environ.get('SECRET_KEY')#.encode()


@app.route('/')
def home():
    return redirect(url_for('all_donations'))

@app.route('/donations/')
def all_donations():
    
    return render_template('donations.jinja2', donations=Donation.select())

@app.route('/lookup/', methods=['GET', 'POST'])
def lookup():
    
    if 'username' not in session:
        return redirect(url_for('login'))

    else:
        return render_template('lookup.jinja2')
    
#    except:
#        return redirect(url_for('exists'))
    
#    else:
#        return render_template('create.jinja2')

@app.route('/create/', methods=['GET', 'POST'])
def create():
    
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
    
        try:
            n = request.form['name']
            v = request.form['donation']
            n = Donor(name=n)
            n.save()
            Donation(donor=n, value=v).save()
    
            return redirect(url_for('all_donations'))
            
        except:
            n = request.form['name']
            #print("exception", n, v)
            return render_template('lookup.jinja2', donor=n, donations=Donation.select())
    
    else:
        return render_template('create.jinja2')
    

@app.route('/login/', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        user = User.select().where(User.name == request.form['name']).get()
        
        if user and pbkdf2_sha256.verify(request.form['password'], user.password):
            session['username'] = request.form['name']
            return redirect(url_for('all_donations'))
        
        return render_template('login.jinja2', error='Incorrect username or password.')
    
    else:
        return render_template('login.jinja2')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)