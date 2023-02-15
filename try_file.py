
# with open(r"C:\Users\User\Downloads\12.png", "rb") as f:
#     text = f.read()
#     #print(text)
# temp = "lol".encode()+text
# print(temp[:3].decode())
# with open(r"C:\Users\User\Downloads\new2.png", "wb") as f:
#     f.write(temp[3:])

# import socket
# tmp = socket.gethostbyname(socket.gethostname())
# print((tmp))

# import queue

# q = queue.Queue()
# print(q.get())

import database as db
tmp = db.users_db("try.db")
tmp.add_client("omer","1.18.52.1","aaaa")
tmp.add_client("tom","1.2.9.1","bbbbb")
tmp.add_client("hi","1.9.11.3","ccccc")
a= tmp.get_user_by_single_info("1.2.9.1",3)
print(a)
print(111111111,tmp.get_specific_stat_from_all_users(3))

