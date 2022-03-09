import mysql.connector

connector = mysql.connector.connect(user='root',
                                    password='2yuhly',
                                    host='localhost',
                                    database='arnetminer',
                                    auth_plugin='mysql_native_password')
cursor = connector.cursor()

# 对前 1w 条数据分析
cursor.execute("create table if not exists `a2pTop` select * from author2paper2 where `author_id` < 6000")
cursor.execute("")
connector.commit()
# cursor.execute("""select `author_id` from author2paper where `index` < 10000""")
cursor.execute("select `author_id` from a2pTop")
result = cursor.fetchall()
author_list = set()
for line in result:
    author_list.add(line[0])
author_list = [_id for _id in author_list]
out = open('output/nodes.txt', 'w')
out.write('index\tauthor_id\n')
for i in range(len(author_list)):
    out.write('%d\t' % i)
    out.write('%d\n' % author_list[i])
out.close()

def getNodeNeighbour(author):
    query_sql = """select `author_id` from a2pTop
    where `paper_id` in (
        select `paper_id` from a2pTop
            where `author_id` = %s
    )
    """
    try:
        cursor.execute(query_sql, (author,))
        result = cursor.fetchall()
    except BaseException as err:
        print('errMsg:', err)
    neighbour = {row[0] for row in result}
    return neighbour
def computeSalton():
    out = open('output/edges.txt', 'w')
    out.write('index\tauthor1_id\tauthor2_id\tsalton\n')
    vectors = open('output/vectors.txt', 'w')
    error_log = open('output/error_los.txt', 'w')
    n = len(author_list)
    data = [[0]*n for i in range(n)]
    index = 0
    for i in range(n):
        for j in range(i):
            data[i][j] = data[j][i]
        for j in range(i, n):
            if i == j:
                salton = 1.0
            else:
                # if i != author_list[i] or j != author_list[j]:
                #     error_log.write('i\tauthor_list[i]\tj\tauthor_list[j]\n')
                s1 = getNodeNeighbour(author_list[i])
                s2 = getNodeNeighbour(author_list[j])
                print('set ij', s1, s2, i, j, end=',')
                salton = len(s1 & s2)/pow(len(s1)*len(s2), 0.5)
                print(salton)
                data[i][j] = salton
            out.write('%d\t%d\t%d\t%d\n' % (index, author_list[i], author_list[j], salton))
            index += 1
        # 写入vector
        for j in range(n-1):
            vectors.write('%d\t' % data[i][j])
        vectors.write('%d\n' % data[i][n-1])
    out.close()
    vectors.close()
    error_log.close()


computeSalton()
