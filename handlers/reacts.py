from config.dbconfig import pg_config
import psycopg2
from flask import jsonify
from daos.reacts import ReactsDAO
from daos.posts import PostsDAO

class ReactHandler:

    def build_react_dict(self, row):
        react_list = {'react_id': row[0], 'react_type': row[1], 'react_date': row[2], 'user_that_react': row[3],
                      'p_reacted': row[4], 'reply_reacted': row[5]}
        return react_list

    def build_react_attributes(self, react_id, react_type, react_date, user_that_react, p_replied, reply_reacted):
        result = {'react_id': react_id, 'react_type': react_type, 'react_date': react_date,
                  'user_that_react': user_that_react, 'p_replied': p_replied, 'reply_reacted': reply_reacted}

        return result

    def getAllReacts(self):
        dao = ReactsDAO()
        react_list = dao.getAllReacts()
        result_list = []
        for row in react_list:
            result = self.build_react_dict(row)
            result_list.append(result)
        return jsonify(React=result_list)

    def getReactById(self, react_id):
        dao = ReactsDAO()
        row = dao.getReactById(react_id)
        if not row:
            return jsonify(Error="React not found."), 404
        else:
            react = self.build_react_dict(row)
            return jsonify(React=react)

    def getReactByDate(self, react_date):
        dao = ReactsDAO()
        return jsonify(React=dao.getReactByDate(react_date))

    def getReactsOnPost(self, post_id, react_type):
        dao = ReactsDAO()
        PostsDAO().getPostById(post_id)
        return jsonify(React=dao.getReactsOnPost(post_id, react_type))

    def createReact(self):
      print("TODO")

    def updateReact(self):
      print("TODO")

    def deleteReact(self):
      print("TODO")

