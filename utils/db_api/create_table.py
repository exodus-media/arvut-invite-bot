from utils.db_api.postgresql import db


async def create_table_users():
    sql = """ 
    CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    my_list INTEGER[],
    black_list INTEGER[],
    language VARCHAR(255) NOT NULL,
    count_pool INT DEFAULT 0,
    login VARCHAR(255),
    password VARCHAR(512),
    PRIMARY KEY (id))
    """
    await db.pool.execute(sql)


async def create_test_users():
    for i in range(20):
        await db.add_user(id=i+1,
                          name='test_user_{}'.format(str(i+1)),
                          language='en')
    for i in range(21, 40):
        await db.add_user(id=i+1,
                          name='test_user_{}'.format(str(i+1)),
                          language='en')


async def run():
    await create_table_users()
    # try:
    #     await create_test_users()
    # except:
    #     return

