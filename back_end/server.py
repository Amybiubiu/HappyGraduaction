import time

import pymysql
from flask import Flask, request, jsonify
import sys, os

app = Flask(__name__)
# CORS(app)

# connector = None
# cnx = mysql.connector.connect(user='root',auth_plugin='mysql_native_password')


#
# @app.before_request
# def before_request_func():
#     cnx.reconnect()


@app.route("/")
def index():
    # print('1')
    print("Printed immediately.")
    # time.sleep(5)
    print("Printed after 5 seconds.")
    return jsonify({"msg": 'index route'}), 404


@app.route("/graph")
def graph():
    cnx = pymysql.connect(user='root', password='2yuhly', host='localhost',
                          database='arnetminer',
                          )
    cursor = cnx.cursor()
    # cursor = cnx.cursor(buffered=True)
    try:
        query_nodes = """select sub.id, name, cat.category from subNetAuthor as sub, category as cat 
            where sub.id = cat.id;"""
        cursor.execute(query_nodes)
        nodes_res = cursor.fetchall()
        nodes = [{'id': t[0], 'name': t[1], 'category': t[2]} for t in nodes_res]
        query_edges = """SELECT * FROM arnetminer.subCoauthor;"""
        cursor.execute(query_edges)
        edges_res = cursor.fetchall()
        # print(edges_res[0])
        edges = [{'source': t[0], 'target': t[1], 'value': t[2]} for t in edges_res]
        cursor.close()
        cnx.close()
        return jsonify({'nodes': nodes, 'links': edges})
    except BaseException as err:
        print(f'Unexpected {err}, {type(err)}')
        cursor.close()
        cnx.close()
        return jsonify({'msg': "something error"}), 500
    # response = make_response(json.dumps({'msg': "something error"}))
    # response.headers['Access-Control-Allow-Origin'] = '*'
    # response.headers['Content-Type'] = 'application/json'
    # response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    # response.headers['Access-Control-Allow-Headers'] = "Content-Type"
    # return response


@app.route("/option")
def option():
    cnx = pymysql.connect(user='root', password='2yuhly', host='localhost',
                          database='arnetminer',
                          )
    cursor = cnx.cursor()
    try:
        query = """select id, name from subNetAuthor"""
        cursor.execute(query)
        res = cursor.fetchall()
        items = [{'id': t[0], 'name': t[1]} for t in res]
        cursor.close()
        cnx.close()
        return jsonify(items)
    except BaseException as err:
        print(f'Unexpected {err}, {type(err)}')
        cursor.close()
        cnx.close()
        return jsonify({'msg': 'something error'}), 500


@app.route("/analysis")
def analysis():
    id = request.args.get('id', '')
    # print(f'analysis id: {id}')
    id1, id2 = id.split(',')  # id1 < id2 !!
    cnx = pymysql.connect(user='root', password='2yuhly', host='localhost',
                          database='arnetminer',
                          )
    cursor = cnx.cursor()
    try:
        query_author = """select name, affiliations, published_count, citation_number, interest 
        from subauthor where id in (%s,%s)"""
        cursor.execute(query_author, (id1, id2))
        author_res = cursor.fetchall()
        a1Res = author_res[0]
        a2Res = author_res[1] if len(author_res) > 1 else a1Res
        query_dis = """select distance from distance where id1 = %s and id2 = %s"""
        cursor.execute(query_dis, (id1, id2))
        disRes = cursor.fetchone()
        query_simi = """select similarity from similarity where id1 = %s and id2 = %s"""
        cursor.execute(query_simi, (id1, id2))
        simiRes = cursor.fetchone()
        res = {
            "author": [{"name": a1Res[0], "affiliations": a1Res[1], "pc": a1Res[2], "cn": a1Res[3], "interest": a1Res[4]},
                       {"name": a2Res[0], "affiliations": a2Res[1], "pc": a2Res[2], "cn": a2Res[3], "interest": a2Res[4]}],
            "dis": disRes[0],
            "simi": simiRes[0] if simiRes else -1
        }
        cursor.close()
        cnx.close()
        return jsonify(res)  # , indent=3, ensure_ascii=False
    except BaseException as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(f'Unexpected {err}, {type(err)}')
        cursor.close()
        cnx.close()
        return jsonify({'msg': "something error"}), 500

#
# @app.after_request
# def after_request_func(response):
#     cnx.close()
#     return response


# with app.test_request_context():
#     print(url_for('graph'))
#     print(url_for('option'))
#     print(url_for('analysis', id='1,2'))


if __name__ == '__main__':
    app.debug = True
    app.run()
