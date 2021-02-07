import mariadb
import sys
import random
import string
import datetime
import os
import shutil


def random_pro(size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))


def file_generator(size):
    content = random_pro(size)
    for i in range(0, 10):
        file_name = 'files/file{}.txt'.format(i)
        with open(file_name, 'w') as f:
            f.write(content)


if __name__ == '__main__':
    file_generator(1000000)
    # 2009-10-04 22:23:00

    try:
        conn = mariadb.connect(
            user="root",
            password="1234",
            host="127.0.0.1",
            port=3306,
            database="TESTS"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor()
    cur.execute("DROP TABLE test0")
    cur.execute(
        "CREATE TABLE test0 (ID INT AUTO_INCREMENT,NAME VARCHAR(50),ADDINFO VARCHAR(150),FILEPATH VARCHAR(200),CREATION DATE, PRIMARY KEY(ID));")

    files_count = os.listdir(path="./files")

    for i in range(0, len(files_count)):
        cur.execute(
            "INSERT INTO test0 (NAME,ADDINFO, FILEPATH, CREATION) VALUES (?, ?, ?, ?)",
            (
            f"{files_count[i]}", random_pro(20), f"/home/root/test/{files_count[i]}", datetime.datetime.now()))

        # os.mkdir("/home/yalkinzsun/test")
        #file_name = "/home/yalkinzsun/{files_count[i-1]}"

        # os.rename(f'./files/{files_count[i]}', f'C:\\Users\\Yalki\\Documents\\files\\new{files_count[i]}')
        # shutil.move(f'./files/{files_count[i]}', f'C:\\Users\\Yalki\\Documents\\files\\new{files_count[i]}')

        shutil.copy2(f'./files/{files_count[i]}', f'/home/root/test/new{files_count[i]}')

    cur.execute("SELECT name, addinfo, filepath, creation FROM test0")

    for name, addinfo, filepath, creation in cur:
        print(f"name: {name}, addinfo: {addinfo} filepath: {filepath} creation {creation}")

    conn.close()


