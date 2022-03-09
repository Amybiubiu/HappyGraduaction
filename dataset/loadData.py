# import xml element tree
import xml.etree.ElementTree as ET
from lxml import etree
# import mysql connector
import mysql.connector

# give the connection parameters
# user name is root
# password is empty
# server is localhost
# database name is database
conn = mysql.connector.connect(user='root',
                               password='2yuhly',
                               host='localhost',
                               database='dblp',
                               auth_plugin='mysql_native_password')
# creating the cursor object
c = conn.cursor()

# reading xml file , file name is vignan.xml
parser = etree.XMLParser(dtd_validation=True)
tree = ET.parse('dblp.xml', parser)

# in our xml file student is the root for all
# student data.
articles = tree.findall('article')
create_sql = """CREATE TABLE IF NOT EXISTS `article`(
   `key` VARCHAR(100) NOT NULL,
   `author` VARCHAR(100) NOT NULL,
   `title` VARCHAR(100) NOT NULL,
   `pages` VARCHAR(10),
   `year` VARCHAR(10),
   `volume` VARCHAR(10),
   `journal` VARCHAR(50),
   `number` VARCHAR(10),
   `ee` VARCHAR(200),
   `url` VARCHAR(200),
   PRIMARY KEY ( `key` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

c.execute(create_sql)
conn.commit()

# retrieving the data and insert into table
# i value for xml data #j value printing number of
# values that are stored
try:
    for article, i in zip(articles, range(1, len(articles))):
        key = article.get('key')
        author = article.find('author').text if article.find('author') else ""  # optional
        title = article.find('title').text if article.find('title') else ""
        pages = article.find('year').text
        volume = article.find('volume').text
        journal = article.find('journal').text
        number = article.find('number').text
        ee = article.find('ee').text
        url = article.find('url').text

        # sql query to insert data into database
        insert_sql = """
    INSERT INTO article(key, author, title, pages, volume, journal, number, ee, url) 
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        # executing cursor object
        c.execute(insert_sql, (key, author, title, pages, volume, journal, number, ee, url))
        conn.commit()
        # print("vignan student No-", j, " stored successfully")
except BaseException as err:
    print(f"Unexpected {err}, {type(err)}")
