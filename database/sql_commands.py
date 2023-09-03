import sqlite3
from database import sql_quieries
import asyncio


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("db.sqlite3", check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.loop = asyncio.get_running_loop()

    def sql_create_db(self):
        if self.connection:
            print("Database connected successfully")

        self.connection.execute(sql_quieries.CREATE_USER_TABLE_QUERY)
        self.connection.execute(sql_quieries.CREATE_USER_FORM_QUERY)
        self.connection.execute(sql_quieries.CREATE_FORM_LIKE_QUERY)
        self.connection.execute(sql_quieries.CREATE_REFERENCE_USERS_TABLE_QUERY)
        self.connection.commit()

    async def sql_insert_users(self, telegram_id,
                               username, first_name, last_name):
        result = await self.loop.run_in_executor(
            None,
            lambda: self.cursor.execute(sql_quieries.START_INSERT_USER_QUERY,
                                              (None, telegram_id,
                                               username, first_name, last_name, None)))
        print(result)
        self.connection.commit()
        return result

    # def sql_insert_users(self, telegram_id,
    #                      username, first_name, last_name):
    #     self.cursor.execute(sql_queries.START_INSERT_USER_QUERY,
    #                         (None, telegram_id,
    #                          username, first_name, last_name, None)
    #                         )
    #     self.connection.commit()

    async def sql_admin_select_username_users_table(self):
        self.cursor.row_factory = lambda cursor, row: {
            "telegram_id": row[0],
            "username": row[1],
            "first_name": row[2],
        }
        result = await self.loop.run_in_executor(
            None,
            lambda: self.cursor.execute(
                sql_quieries.SELECT_USER_QUERY
            ).fetchall()
        )
        return result

    # def sql_admin_select_username_users_table(self):
    #     self.cursor.row_factory = lambda cursor, row: {
    #         "telegram_id": row[0],
    #         "username": row[1],
    #         "first_name": row[2],
    #     }
    #     return self.cursor.execute(
    #         sql_quieries.SELECT_USER_QUERY
    #     ).fetchall()

    def sql_insert_user_form(self, telegram_id,
                             nickname, age, bio, photo):
        self.cursor.execute(sql_quieries.INSERT_USER_FORM_QUERY,
                            (None, telegram_id, nickname, age, bio, photo)
                            )
        self.connection.commit()

    def sql_select_user_form_by_telegram_id(self, telegram_id):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "telegram_id": row[1],
            "nickname": row[2],
            "age": row[3],
            "bio": row[4],
            "photo": row[5],
        }
        return self.cursor.execute(
            sql_quieries.SELECT_USER_FORM_BY_TELEGRAM_ID_QUERY, (telegram_id,)
        ).fetchall()

    def sql_select_user_forms(self):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "telegram_id": row[1],
            "nickname": row[2],
            "age": row[3],
            "bio": row[4],
            "photo": row[5],
        }
        return self.cursor.execute(
            sql_quieries.SELECT_USER_FORM_QUERY
        ).fetchall()

    def sql_insert_like_form_command(self, owner_telegram_id, liker_telegram_id):
        self.cursor.execute(sql_quieries.INSERT_LIKE_FORM_QUERY,
                            (None, owner_telegram_id, liker_telegram_id))
        self.connection.commit()

    def sql_liked_form_command(self, owner_telegram_id, liker_telegram_id):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "owner_telegram_id": row[1],
            "liker_telegram_id": row[2],
        }
        return self.cursor.execute(
            sql_quieries.SELECT_LIKED_FORM_QUERY,
            (owner_telegram_id, liker_telegram_id,)
        ).fetchall()

    def update_user_form_command(self, telegram_id,
                                 nickname, age, bio, photo):
        self.cursor.execute(sql_quieries.UPDATE_USER_FORM_QUERY,
                            (nickname, age, bio, photo, telegram_id,)
                            )
        self.connection.commit()

    def sql_delete_user_form_command(self, telegram_id):
        self.cursor.execute(sql_quieries.DELETE_USER_FORM_QUERY,
                            (telegram_id,)
                            )
        self.connection.commit()

    def update_user_by_reference_link_command(self, link, telegram_id):
        self.cursor.execute(sql_quieries.UPDATE_USER_BY_LINK_QUERY,
                            (link, telegram_id,)
                            )
        self.connection.commit()

    def select_existed_link(self, telegram_id):
        self.cursor.row_factory = lambda cursor, row: {
            "link": row[0],
        }
        return self.cursor.execute(
            sql_quieries.SELECT_EXISTED_LINK_QUERY,
            (telegram_id,)
        ).fetchall()

    def select_owner_link_command(self, link):
        self.cursor.row_factory = lambda cursor, row: {
            "telegram-id": row[0],
        }
        return self.cursor.execute(
            sql_quieries.SELECT_LINK_OWNER_QUERY,
            (link,)
        ).fetchall()

    def sql_insert_reference_users_command(self, owner_telegram_id,
                                           reference_telegram_id):
        self.cursor.execute(sql_quieries.INSERT_REFERENCE_USERS_QUERY,
                            (None, owner_telegram_id, reference_telegram_id,)
                            )
        self.connection.commit()