import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime

# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        continue

def add_user(data):
    USERS_REF.add(data)

def delete_user(arg):
    user = find_user('snum', arg)

    if('name' in user):
        print('Result:', user['name'], user['lastname'], user['did'])
        USERS_REF.document(user['did']).delete()
        print('DELETED')
        print()
        return
    
    print('User not found:', arg)

def add_check(uid, time):
    global schema_check
    
    docs = find_checks(uid, 1)

    for doc in docs:
        d = doc.to_dict()
        schema_check['in'] = not d['in']
    
    schema_check['time'] = time
    schema_check['uid'] = uid

    if(schema_check['in'] == True):
        print('Checked IN')
    else:
        print('Checked OUT')

    CHECKS_REF.add(schema_check)


def find_user(field, arg):
    docs = USERS_REF.where(field, '==', arg).stream()

    for doc in docs:
        d = doc.to_dict()
        d['did'] = doc.id

        if(d[field] == arg):
            return d
    
    return {}

def find_user_by_uid(uid):
    #docs = USERS_REF.stream()
    docs = USERS_REF.where('uid', '==', uid).stream()

    for doc in docs:
        d = doc.to_dict()
        if(d['uid'] == uid):
            return d
    
    return {}

def get_all_users():
    return USERS_REF.stream()

def find_checks(uid, num, last=False):
    docs = CHECKS_REF.where('uid', '==', uid).limit(num).order_by('time', direction='DESCENDING').stream()

    return docs

def get_admin():
    doc = ADMIN_REF.document('creds').get()
    d = doc.to_dict()
    
    return d

def set_admin(data):
    ADMIN_REF.document('creds').set(data)

cred = credentials.Certificate("core-lab-reg-firebase-adminsdk-7m4cm-07396b6d94.json")
firebase_admin.initialize_app(cred)

# access the database
database = firestore.client()

USERS_REF = database.collection("users")
CHECKS_REF = database.collection("checks")
ADMIN_REF = database.collection('admin')

schema_check = {
    'in': True,
    'time': '',
    'uid': '0',
}