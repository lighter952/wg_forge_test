import psycopg2
from statistics import mean, median, mode
from models import Cat

conn = psycopg2.connect(host='localhost', port='5432', password='42a', dbname='wg_forge_db', user='wg_forge', )
cur = conn.cursor()


def get_cats_from_db(attribute: str, order: str, offset: int, limit: int) -> list[dict]:
    try:
        cur.execute("SELECT * FROM cats ORDER BY {} {} OFFSET {} LIMIT {}".format(attribute, order, offset, limit))
        res = cur.fetchall()
        print(res)
        json_res = []
        for cat in res:
            record = {"name": cat[0], "color": cat[1], "tail_length": cat[2], "whiskers_length": cat[3]}
            json_res.append(record)
        return json_res
    except IOError:
        print("Get cats from database error!, ")


def append_new_cat_to_db(cat: Cat):
    print(cat)
    try:
        cur.execute("insert into cats (name, color, tail_length, whiskers_length) values (\'{}\',\'{}\',{},{})".format(str(cat.name), str(cat.color).lower(), int(cat.tail_length), int(cat.whiskers_length)))
        conn.commit()
    except IOError:
        print('New cat creation error!')
        return {"Database error, new cat dont create."}


def is_offset_in_range(offset: int) -> True | False:
    """
    Check is offset greater then 0 and less than table size.
    """
    try:
        cur.execute("select count(*) from cats")
        table_size = cur.fetchone()[0]
        if offset >= table_size or offset < 0:
            return False
        return True
    except IOError as e:
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

    cur.execute(f"insert into cats_stat values ({tail_length_mean},{tail_length_median},array[{tail_length_mode}],{whiskers_length_mean},{whiskers_length_median},array[{whiskers_length_mode}]);")
    conn.commit()


def update_cats_color_counts() -> None:
    cur.execute("insert into cat_colors_info (color, count) select color, count(*) as count from cats group by color;")
    conn.commit()

