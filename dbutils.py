#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import config

class DB(object):
    def __init__(self):
        self.conn = sqlite3.connect(config.db_file)
        print('__init__')

    def __del__(self):
        self.conn.close()
        print('__del__')

    def ttest(self):
        # sql_text = '''INSERT INTO notice_t(user_name,user_id,chat_id,message_id) VALUES(?,?,?,?)'''
        
        # project = (query_d['from']['first_name'], query_d['from']['id'], chat_id, message_id)
        # cur.execute(sql_text, project)
        self.conn.commit()

    def get_notice_cnt(self, user_id):
        return 3

    # Пытаемся узнать из базы «состояние» пользователя
    def get_user_state(self, user_id):
        SQL_SELECT_S = '''select u.state from user_t u where u.tele_user_id = :user_id'''
        # sql_s = '''select u.state from user_t u where u.tele_user_id = :user_id'''
        conn = sqlite3.connect(config.db_file)
        row = conn.cursor().execute(SQL_SELECT_S, {"user_id": user_id}).fetchone()
        # row = conn.cursor().execute(sql_s, {"user_id": user_id}).fetchone()
        state_s = config.States.START_S
        if row:
            state_s = row[0]
        else:
            print('get_user_state.row is None')
        conn.close()
        print('get_user_state.state_s={state_s}'.format(state_s=state_s))
        return state_s

    def set_user_state(self, user_id, value_s, user_name_s):
        SQL_CNT_S = '''
            select count() as cnt from user_t u where u.tele_user_id = :user_id
            '''
        SQL_INSERT_S = '''
            insert into user_t (tele_user_id, state, tele_user_name) values(:user_id, :state, :user_name)
            '''
        SQL_UPDATE_S = '''
            update user_t set state = :state, tele_user_name = :user_name where tele_user_id = :user_id
            '''
        conn = sqlite3.connect(config.db_file)
        cur = conn.cursor()
        cnt = cur.execute(SQL_CNT_S, {"user_id": user_id}).fetchone()[0]
        print(cnt)
        sql_text_s = SQL_UPDATE_S
        if cnt == 0:
            sql_text_s = SQL_INSERT_S
        cur.execute(sql_text_s, {"user_id": user_id, "state": value_s, "user_name": user_name_s})
        conn.commit()
        conn.close()
        print('set_user_state')

