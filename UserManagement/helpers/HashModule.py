import string, random, hashlib

#generate random salt of random length 
def randomSalt(length):
    letters = string.ascii_letters 
    return "".join(random.choice(letters) for i in range(length))

#hash password
def hashPassword(password):
    return hashlib.sha512(str(password).encode("UTF-8")).hexdigest()

#encrypt password using hash and salt
def encryptPassword(password, salt):
    return hashlib.sha512(str(hashPassword(password) + salt).encode("UTF-8")).hexdigest()