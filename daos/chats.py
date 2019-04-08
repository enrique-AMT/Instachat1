from config.dbconfig import pg_config
from flask import jsonify
import psycopg2

class ChatsDAO:
  def __init__(self):
    connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                                pg_config['user'],
                                                                pg_config['passwd'], pg_config['host'])

    self.conn = psycopg2._connect(connection_url)

  def getAllChats(self):
    cursor = self.conn.cursor()
    query = "select * from instachat.chat;"

    # select chat_id, chat_name, owner_id, count(u_belongs) from instachat.chat natural inner join instachat.belongs " \
    #         "group by chat_id, chat_name, owner_id;

    cursor.execute(query)
    result = []
    for row in cursor:
      result.append(row)
    return result

  def getChatById(self, chat_id):
    cursor = self.conn.cursor()
    cursor.execute("select * from instachat.chat where chat_id = %s;", [chat_id])

    # "select chat_id, chat_name, owner_id, count(u_belongs) from instachat.chat natural inner join instachat.belongs"
    # " where chat_id = %s group by chat_id, chat_name, owner_id;", [chat_id]

    result = cursor.fetchone()
    return result

  def getChatUsers(self, chat_id):
    cursor = self.conn.cursor()
    chat_list = self.getAllChats()
    if len(chat_list) < chat_id or chat_id < 1:
      return jsonify(Error='Chat not found'), 404
    cursor.execute("select user_id, first_name, last_name from instachat.user natural inner join instachat.chat "
                   "where chat_id = %s and user_id in (select u_belongs from instachat.belongs "
                   "where c_user_belongs = %s);", [chat_id, chat_id])


    # "select user_id, first_name, last_name, count(u_belongs) from instachat.chat natural inner join instachat.belongs "
    # "natural inner join instachat.user where chat_id = %s and user_id in (select u_belongs from instachat.belongs"
    # " where chat_id = %s) group by user_id, first_name, last_name;", [chat_id, chat_id]

    result = []
    for row in cursor:
        result.append(row)
    return result

  def getChatOwner(self, chat_id):
    cursor = self.conn.cursor()
    cursor.execute("select user_id, first_name, last_name from instachat.user natural inner join instachat.chat "
                   "where chat_id = %s and user_id in (select owner_id from instachat.chat where chat_id = %s);",
                   [chat_id, chat_id])
    result = []
    for row in cursor:
        result.append(row)
    return result


