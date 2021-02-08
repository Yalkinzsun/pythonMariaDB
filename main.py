import mariadb
import sys
import random
import string
import datetime
import os
import shutil
import time


def random_pro(size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))


def file_generator(num_of_files, content_size):
    content = random_pro(content_size)
    for i in range(0, num_of_files):
        file_name = 'files/file{}.txt'.format(i)
        with open(file_name, 'w') as f:
            f.write(content)


if __name__ == '__main__':
    file_generator(900, 1000000)
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

    files_count = os.listdir(path="./files")
    files_count_len = len(files_count)

    for p in [1, 2, 3]:
        cur.execute("DROP TABLE IF EXISTS test0")
        cur.execute(
            "CREATE TABLE test0 (ID INT AUTO_INCREMENT, NAME VARCHAR(50), ADDINFO VARCHAR(150), FILEPATH VARCHAR(200), CREATION DATE, PRIMARY KEY(ID));")
        start_time = time.time()
        for i in range(0, int(files_count_len / 3) * p):
            cur.execute(
                "INSERT INTO test0 (NAME, ADDINFO, FILEPATH, CREATION) VALUES (?, ?, ?, ?)",
                (f"{files_count[i]}", random_pro(20), f"/home/root/test/{files_count[i]}",
                 datetime.datetime.now())
            )

        end_time = time.time()
        print(f'Время записи {(files_count_len / 3) * p} строк данных в бд: {end_time - start_time} сек')


        start_copy_time = time.time()
        for i in range(0, int(files_count_len / 3) * p):
            #shutil.copy2(f'./files/{files_count[i]}', f'C:\\Users\\Yalki\\Documents\\files\\new{files_count[i]}')
            shutil.copy2(f'./files/{files_count[i]}', f'/root/test/new{files_count[i]}')
        end_copy_time = time.time()
        print(f'Время копирования {(files_count_len / 3) * p} файлов в вайловую систему: {end_copy_time - start_copy_time} сек.')


        start_read_time = time.time()
        cur.execute("SELECT name, addinfo, filepath, creation FROM test0")
        for name, addinfo, filepath, creation in cur:
            pass
            # print(f"name: {name}, addinfo: {addinfo} filepath: {filepath} creation {creation}")
        end_read_time = time.time()
        print(
            f'Время чтения {(files_count_len / 3) * p} записей из бд: {end_read_time - start_read_time} сек.')
        print("-" * 15)
    conn.close()

