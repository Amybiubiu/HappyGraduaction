import mysql.connector

connector = mysql.connector.connect(user='root',
                                    password='2yuhly',
                                    host='localhost',
                                    database='arnetminer',
                                    auth_plugin='mysql_native_password')
cursor = connector.cursor()

# create_sql1 = """CREATE TABLE IF NOT EXISTS `author`(
#     `index` INT NOT NULL,
#     `name` VARCHAR(100) NOT NULL,
#     `affiliations` VARCHAR(200) NOT NULL,
#     `published_count` TINYINT NOT NULL,
#     `citation_number` TINYINT NOT NULL,
#     `hi` INT NOT NULL,
#     `pi` FLOAT NOT NULL,
#     `upi` FLOAT NOT NULL,
#     `interest` TEXT NOT NULL,
#     PRIMARY KEY (`index`)
# )ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
alter_sql1 = "ALTER TABLE `author` CHANGE `pi` `pi` DOUBLE NOT NULL,CHANGE `upi` `upi` DOUBLE NOT NULL"

create_sql2 = """CREATE TABLE IF NOT EXISTS `paper`(
    `index` INT NOT NULL,
    `title` CHAR(100) NOT NULL,
    `authors` CHAR(255),
    `affiliations` TEXT,
    `year` CHAR(4),
    `publication_venue` CHAR(255),
    `references_id` INT,
    `abstract` TEXT,
    PRIMARY KEY (`index`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

create_sql3 = """CREATE TABLE IF NOT EXISTS `coauthor`(
    `index_a` INT NOT NULL,
    `index_b` INT NOT NULL,
    `number` INT,
    primary key(`index_a`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

create_sql4 = """CREATE TABLE IF NOT EXISTS `author2paper`(
    `index` INT NOT NULL,
    `author_id` INT NOT NULL,
    `paper_id` INT NOT NULL,
    `author_position` INT NOT NULL,
    primary key(`index`)
)"""
# cursor.execute(alter_sql1)
# cursor.execute(create_sql2)
# cursor.execute(create_sql3)
# cursor.execute(create_sql4)
# connector.commit()

# Author2Paper = open('/Users/mac/downloads/dataset/AMiner-Author2Paper.txt')
# for line in Author2Paper:
#     row = line.strip().split('\t')
#     print(row)
#     index, author_id, paper_id, author_position = row[0], row[1], row[2], row[3]
#     try:
#         insert_sql = """INSERT INTO author2paper VALUES(%s, %s, %s, %s)"""
#         cursor.execute(insert_sql, (index, author_id, paper_id, author_position))
#         connector.commit()
#         print('insert into author2paper table, the index is %s' % index)
#     except BaseException as err:
#         # print(f"Unexpected {err}, {type(err)}")
#         print('insert row into coauthor table failed, the index of row is %s' % index)


# Author = open('/Users/mac/downloads/dataset/AMiner-Author.txt')
# author = {}
# for line in Author:
#     if line.startswith('#index'):
#         author['index'] = line.strip().split(' ')[1]
#     elif line.startswith('#n'):
#         author['name'] = line[3:].strip()
#     elif line.startswith('#a'):
#         author['affiliations'] = line[3:].strip()
#     elif line.startswith('#pc'):
#         author['published_count'] = line.strip().split(' ')[1]
#     elif line.startswith('#cn'):
#         author['citation_number'] = line.strip().split(' ')[1]
#     elif line.startswith('#hi'):
#         author['hi'] = line.strip().split(' ')[1]
#     elif line.startswith('#pi'):
#         author['pi'] = line.strip().split(' ')[1]
#     elif line.startswith('#upi'):
#         author['upi'] = line.strip().split(' ')[1]
#     elif line.startswith('#t'):
#         author['interest'] = line[3:].strip()
#     else:
#         try:
#             insert_sql = """INSERT INTO author VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#             cursor.execute(insert_sql, (author['index'], author['name'], author['affiliations'],
#                                     author['published_count'], author['citation_number'],
#                                     author['hi'], author['pi'], author['upi'], author['interest']))
#             connector.commit()
#             print('insert row into author table, the index of row is %s' % author['index'])
#             author.clear()
#         except BaseException as err:
#             print(f"Unexpected {err}, {type(err)}")
#             print('insert row into author table failed, the index of row is %s' % author['index'])
# Author.close()

# Paper = open('/Users/mac/downloads/dataset/AMiner-Paper.txt')
# paper = {}
# paper['references_id'] = ''
# for line in Paper:
#     if line.startswith('#index'):
#         paper['index'] = line.strip().split(' ')[1]
#     elif line.startswith('#*'):
#         paper['title'] = line[3:].strip()
#     elif line.startswith('#@'):
#         paper['authors'] = line[3:].strip()
#     elif line.startswith('#o'):
#         paper['affiliations'] = line[3:].strip()
#     elif line.startswith('#t'):
#         paper['year'] = line.strip().split(' ')[1]
#     elif line.startswith('#c'):
#         paper['publication_venue'] = line[3:].strip()
#     elif line.startswith('#%'):
#         paper['references_id'] += line.strip().split(' ')[1] + ', '
#     elif line.startswith('#!'):
#         paper['abstract'] = line[3:].strip()
#     else:
#         try:
#             insert_sql = """INSERT INTO paper VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#             cursor.execute(insert_sql, (paper['index'], paper['title'], paper['authors'], paper['affiliations'],
#                                         paper['year'], paper['publication_venue'], paper['references_id'],
#                                         paper['abstract']))
#             connector.commit()
#             print('insert row into paper table, the index of row is %s' % paper['index'])
#             paper.clear()
#         except BaseException as err:
#             print(f"Unexpected {err}, {type(err)}")
#             print('insert row into paper table failed, the index of row is %s' % paper['index'])
# Paper.close()

Coauthor = open('/Users/mac/downloads/dataset/AMiner-Coauthor.txt').readlines()
coauthor = {}
for line, i in zip(Coauthor, range(len(Coauthor))):
    data = line[1:].strip().split('\t')
    index_a, index_b, number = data[0], data[1], data[2]
    try:
        insert_sql = """INSERT INTO coauthor VALUES(%s, %s, %s)"""
        cursor.execute(insert_sql, (index_a, index_b, number))
        connector.commit()
        if i/100 == 0:
            print('insert row into coauthor table, the index_a of row is %s' % index_a)
    except BaseException as err:
        print(f"Unexpected {err}, {type(err)}")
        print('insert row into coauthor table failed, the index of row is %s' % index_a)
Coauthor.close()
