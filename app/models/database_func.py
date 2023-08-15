from types import NoneType
import os
import psycopg2
from statistics import mean, median, mode
from fastapi import HTTPException
from app.schemas.cats import Cat


# db_host = os.getenv("DB_HOST")
# db_port = os.getenv("DB_POST")
# db_name = os.getenv("DB_NAME")
# db_user = os.getenv("DB_USER")
# db_pass = os.getenv("DB_PASS")

db_host = '0.0.0.0'
db_port = 5432
db_name = 'wg_forge_db'
db_user = 'wg_forge'
db_pass = '42a'

conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    password=db_pass,
    dbname=db_name,
    user=db_user
)
cur = conn.cursor()


def get_user_hash(user_id: int) -> str:
    cur.execute(f'SELECT * FROM user_passwords WHERE user_id = \'{user_id}\'')
    user_hash = cur.fetchone()
    if type(user_hash) is NoneType:
        return '0'
    return user_hash[2]


def update_password_hash(user_id: int, new_hash: str) -> int:
    cur.execute("UPDATE user_passwords SET password_hash = \'{}\' WHERE user_id = {}".format(new_hash, user_id))
    conn.commit()
    return 200


def get_user_from_bd(username: str) -> dict:
    try:
        cur.execute("SELECT * FROM users WHERE username = \'{}\'".format(username))
        user_from_bd = cur.fetchone()
        if type(user_from_bd) is NoneType:
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        return {
            "user_id": "{}".format(user_from_bd[0]),
            "username": "{}".format(user_from_bd[1]),
            "full_name": "{}".format(user_from_bd[2]),
            "email": "{}".format(user_from_bd[3]),
            "disabled": user_from_bd[4]
        }
    except IOError:
        print("Get user from database error!")


def get_cats_from_db(attribute: str, order: str, offset: int, limit: int) -> list[dict]:
    try:
        cur.execute("SELECT * FROM cats ORDER BY {} {} OFFSET {} LIMIT {}".format(attribute, order, offset, limit))
        res = cur.fetchall()

        json_res = []
        for cat in res:
            record = {"name": cat[0], "color": cat[1], "tail_length": cat[2], "whiskers_length": cat[3]}
            json_res.append(record)
        return json_res
    except IOError:
        print("Get cats from database error!")


def append_new_cat_to_db(cat: Cat):
    print(cat)
    try:
        cur.execute("insert into cats (name, color, tail_length, whiskers_length) values (\'{}\',\'{}\',{},{})".format(
            str(cat.name), str(cat.color).lower(), int(cat.tail_length), int(cat.whiskers_length)))
        conn.commit()
    except IOError:
        print('New cat creation error!')
        return {"Database error, new cat dont create."}


def is_offset_in_range(offset: int) -> True | False:
    """
    Check is offset greater than 0 and less than table size.
    """
    try:
        cur.execute("select count(*) from cats")
        table_size = cur.fetchone()[0]
        if offset >= table_size or offset < 0:
            return False
        return True
    except IOError:
        print("Check is offset in range error!")


def update_cats_stat() -> None:
    """
    Update statistic information in cats_stat table.
    """
    cur.execute('select tail_length, whiskers_length  from cats;')
    res = cur.fetchall()

    tail_lengths, whiskers_length = zip(*res)

    tail_length_mean: float = mean(tail_lengths)
    tail_length_median: float = median(tail_lengths)
    tail_length_mode: int = mode(tail_lengths)
    whiskers_length_mean: float = mean(whiskers_length)
    whiskers_length_median: float = median(whiskers_length)
    whiskers_length_mode: int = mode(whiskers_length)

    cur.execute(
        f"insert into cats_stat values ({tail_length_mean},{tail_length_median},array[{tail_length_mode}],\
        {whiskers_length_mean},{whiskers_length_median},array[{whiskers_length_mode}]);")
    conn.commit()


def update_cats_color_counts() -> None:
    cur.execute("insert into cat_colors_info (color, count) select color, count(*) as count from cats group by color;")
    conn.commit()
