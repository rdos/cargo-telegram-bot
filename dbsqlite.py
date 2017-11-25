#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3


class DB:
	def __init__(self):
		print('__init__')

	def ttest(self):
		conn = sqlite3.connect('cargo.sqlite')
		sql_text = '''INSERT INTO notice_t(user_name,user_id,chat_id,message_id) VALUES(?,?,?,?)'''
		cur = conn.cursor()
		# project = (query_d['from']['first_name'], query_d['from']['id'], chat_id, message_id)
		# cur.execute(sql_text, project)
		conn.commit()
		conn.close()
