from os import system, name
import getpass, time, shutil, csv, hashlib, os
import hashlib, binascii
import re


 
def main():
    clear()
    print("----Welcome to BDMS v1.0----")
    print()
    print("1. Login to account")
    print("2. Register as new user")
    c = int(input("Enter choice: "))
    if c==1:
        login()
    elif c==2:
        register()
    else:
        print("Bad input, redirecting...")
        time.sleep(2)
        main()

def login():
    clear()
    print("------Login Page------")
    print("Enter credentials")
    print()
    
    email = input("Email: ")
    passwd = getpass.getpass(prompt="Password: ")
    
    with open('users.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            salt = row[3][:64]
            key = row[3][64:]
            pwdhash = hashlib.pbkdf2_hmac('sha256', 
                                  passwd.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
            pwdhash = binascii.hexlify(pwdhash).decode('ascii')
            
            if pwdhash == key and email == row[0]:
                print('Login successful, redirecting...')
                time.sleep(2)
                home(email)
                return 0
                
    print("Email and/or password is incorrect")
    print("Try again")
    time.sleep(2)
    login()
    return 0
            
    
    

def register():
    clear()
    print("Enter the following details to register: ")
    email = input("Email id: ")
    
    rowcount = 0
    
    with open('users.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0] == email:
                print("\n\nEmail already exists, please try again")
                time.sleep(2)
                register()
                return 0
            else:
                rowcount+=1
    
    name = input("Name: ")
    mobile = int(input("Mobile number (10 digits): "))
    pass1 = getpass.getpass(prompt="Password: ")
    pass2 = getpass.getpass(prompt="Confirm password: ")
    
    if pass1 != pass2:
        print("\n\nPasswords do not match, please try again")
        time.sleep(2)
        register()
        return 0
    
    sex = input("Sex (M/F/N): ")
    
    city = input("City: ")
    
    print("1. Use default profile picture")
    print("2. Enter path of profile picture")
    c = int(input("Enter your choice: "))
    path = "profile_pictures/default.jpg"
    if c==2:
        path = input("Enter path (only .jpg supported): ")
        shutil.copy(path, "profile_pictures/"+name+"_"+str(rowcount)+".jpg")
        path = "profile_pictures/"+name+"_"+str(rowcount)+".jpg"
    
    salt = hashlib.sha256(os.urandom(32)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha256', pass1.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    storage = (salt + pwdhash).decode('ascii')
    
    f = open("users.csv", "a")
    f.write('"'+email+'"'+','+name+','+str(mobile)+',')
    f.close()
    
    f = open("users.csv", "a")
    f.write(storage)
    f.close()
    
    f = open("users.csv", "a")
    f.write(','+sex+','+city+','+path+','+str(rowcount)+'\n')
    f.close()
    
       
    login()

def home(email):
    clear()
    print("----Welcome to BDMS v1.0----")
    print()
    with open('users.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if email == row[0]:
                print("Email: "+email)
                print("Name: "+row[1])
                print("Mobile: "+row[2])
                print("Sex: "+row[4])
                print("City: "+row[5])
                break
    print("\n\n")
    print("Find users")
    name = input("Enter name to search: ")
    
    ctr=0
    with open('users.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if re.search(name, row[1], re.IGNORECASE):      #searching for substring since people can have same first name 
                ctr=1
                print()
                print("Email: "+row[0])
                print("Name: "+row[1])
                print("Mobile: "+row[2])
                print("Sex: "+row[4])
                print("City: "+row[5])
                print()
                
    if ctr==0:
        print("Not found")
    
    
    
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
  
 
main()