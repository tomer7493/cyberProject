from datetime import datetime
import sqlite3


class users_db:
    def __init__(self, path="\\", tablename="Users_Table", col_client_name="client_name", col_ip_addr="ip_addr", col_mac_addr="mac_addr"):
        self.path = path
        self.tablename = tablename
        self.col_client_name = col_client_name
        self.col_ip_addr = col_ip_addr
        self.col_mac_addr = col_mac_addr
        conn = sqlite3.connect(self.path)
        conn.execute(
            f'CREATE TABLE IF NOT EXISTS {self.tablename} (id INTEGER PRIMARY KEY, {self.col_client_name} STRING,{self.col_mac_addr} STRING,{self.col_ip_addr} STRING )')
        conn.commit()
        conn.close()

    def add_client(self, client_name, ip_addr, mac_addr):
        conn = sqlite3.connect(self.path)
        str_insert = f"INSERT INTO {self.tablename} ({self.col_client_name},{self.col_ip_addr},{self.col_mac_addr}) VALUES ('{client_name}','{ip_addr}','{mac_addr}')"
        try:
            conn.execute(str_insert)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(e)
            return False

    def get_specific_stat_from_all_users(self, mode: int):
        '''
        ---for name enter mode 1 
        ---for mac  enter mode 2
        ---for ip   enter mode 3 
       '''

        if (mode == 1):
            info_col = self.col_client_name
        elif (mode == 2):
            info_col = self.col_mac_addr
        elif (mode == 3):
            info_col = self.col_ip_addr
        else:
            return []

        conn = sqlite3.connect(self.path)
        cursor = conn.execute(
            f"SELECT {info_col} FROM {self.tablename}")
        data = cursor.fetchall()
        conn.close()
        if (data == []):
            return data
        ret_list = []
        for user in data:
            ret_list.append(user[0])
        return ret_list

    def get_user_by_single_info(self, info: str, mode: int):
        '''
        ---for name enter mode 1 
        ---for mac  enter mode 2
        ---for ip   enter mode 3 
       '''

        if (mode == 1):
            info_col = self.col_client_name
        elif (mode == 2):
            info_col = self.col_mac_addr
        elif (mode == 3):
            info_col = self.col_ip_addr
        else:
            return []

        conn = sqlite3.connect(self.path)
        cursor = conn.execute(
            f"SELECT * FROM {self.tablename} WHERE {info_col} = '{info}'")
        data = cursor.fetchall()
        conn.close()
        if (data == []):
            return data
        return data[0][1:]
