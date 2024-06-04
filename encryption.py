import hashlib


def hash_password(password:str):
    password_bytes = password.encode('utf-8')
    hashed_password = hashlib.sha256(password_bytes).hexdigest()
    return hashed_password

def check_password(password:str, hashed_password:str):
    if hash_password(password) == hashed_password:
        print("Logged in successfully.")
        return True
    else:
        print("Incorrect password")
        return False



# while True:
#     password = input("Enter your password:")
#     # hashed_password = hash_password(password)
#     # print("Hashed password:", hashed_password)
    
#     if check_password(password):
#         break
#     print("*"*20)

