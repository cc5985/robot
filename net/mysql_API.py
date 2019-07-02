#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql


class MySQLManager:

    def __init__(self,user_name="root", password="", schema=None, target_server_ip="localhost", port=3306):

        try:
            self.db_name=schema
            self.db=pymysql.connect(target_server_ip,user_name,password,schema,port=port)
            self.db.connect_timeout=10000
        except Exception as e:
            print(e)

    def reconnect(self, user_name, password, schema):
        self.db.close()
        try:
            self.db=pymysql.connect("localhost",user_name,password,schema)
        except Exception as e:
            return e

    def create_table(self, table_name, args, drop_table=False):
        cursor = self.db.cursor()
        try:
            sql = """CREATE TABLE """ + table_name + """ (""" + args +")"
            # FIRST_NAME  CHAR(20) NOT NULL,
            # LAST_NAME  CHAR(20),
            # AGE INT,
            # SEX CHAR(1),
            # INCOME FLOAT )
            cursor.execute(sql)
            return True
        except Exception as e:
            print("Error: " + str(e))
            return False

    def insert_data(self, sql_string):
        cursor = self.db.cursor()
        # sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
        #  LAST_NAME, AGE, SEX, INCOME)
        #  VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
        try:
            # 执行sql语句
            cursor.execute(sql_string)
            # 提交到数据库执行
            self.db.commit()
            return True
        except Exception as e:
            # 如果发生错误则回滚
            self.db.rollback()
            print("Error: " + str(e))
            return False



    def update_date(self, table_name):
        pass

    def inquire(self, sql_string):
        cursor=self.db.cursor()
        try:
            cursor.execute(sql_string)
            return cursor.fetchall()
        except Exception as e:
            print("Error: " + str(e))
            return False


    def execute(self, sql_string):
        cursor=self.db.cursor()
        try:
            cursor.execute(sql_string)
            return cursor.fetchall()
        except Exception as e:
            print("Error: " + str(e))
            return False

    def len_of_table(self, table_name, unit="MB"):
        try:

            sql_string="""select concat(round(sum(DATA_LENGTH/1024/1024),2),'M') from tables where table_schema=’""" + self.db_name + """’ AND table_name=’""" + table_name + """’;"""
            print(sql_string)
            cursor=self.db.cursor()
            cursor.execute(sql_string)
            b=cursor.fetchall()
            #
            # if unit.lower()=="byte":
            #     pass
            # elif unit.lower()=="kb":
            #     b/=1024
            # elif unit.lower()=="mb":
            #     b/=1048576
            return b
        except Exception as e:
            return "Error: " + str(e)




    def len_of_schema(self, schema_name, unit="MB"):
        try:
            sql_string="SELECT sum(DATA_LENGTH)+sum(INDEX_LENGTH) FROM information_schema.TABLES where TABLE_SCHEMA='" + schema_name  + "'; "
            cursor=self.db.cursor()
            cursor.execute(sql_string)
            b=cursor.fetchall()[0][0]
            if unit.lower()=="byte":
                pass
            elif unit.lower()=="kb":
                b/=1024
            elif unit.lower()=="mb":
                b/=1048576
            return b
        except Exception as e:
            return "Error: " + str(e)


    def close(self):
        self.db.close()

    # def if_table_exists(self,table_name):
    #     query_string='SELECT TABLE_NAME FROM ' + self.db_name + '.TABLES WHERE TABLE_SCHEMA=' + self.db_name + ' AND TABLE_NAME=' + table_name
    #     cursor=self.db.cursor()

'''
# 打开数据库连接
db = pymysql.connect("localhost","root","caichong","test" )

print(db)
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()

print ("Database version : %s " % data)

# 关闭数据库连接
db.close()
'''

'''
create a new table

# 打开数据库连接
db = pymysql.connect("localhost","root","caichong","test" )

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute() 方法执行 SQL，如果表存在则删除
cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

# 使用预处理语句创建表
sql = """CREATE TABLE EMPLOYEE (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,  
         SEX CHAR(1),
         INCOME FLOAT )"""

cursor.execute(sql)

# 关闭数据库连接
db.close()

'''

