import random

from model import db, Donor, Donation, User 
from passlib.hash import pbkdf2_sha256

db.connect()

# This line will allow you "upgrade" an existing database by
# dropping all existing tables from it.
db.drop_tables([Donor, Donation, User])

db.create_tables([Donor, Donation, User])

alice = Donor(name="Alice")
alice.save()
Donation(donor=alice, value=100).save()

bob = Donor(name="Bob")
bob.save()
Donation(donor=bob, value = 200).save()

charlie = Donor(name="Charlie")
charlie.save()
Donation(donor=charlie, value=300).save()

User(name='admin', password=pbkdf2_sha256.hash('password')).save()

#donors = [alice, bob, charlie]
#
#for x in range(30):
#    Donation(donor=random.choice(donors), value=random.randint(100, 10000)).save()
    
#karl = Donor(name='Karl').save()
    #q = Donor.select()
    #for i in q:
        #print(i.name)