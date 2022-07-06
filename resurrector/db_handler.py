# provides different functions such as :
# creating a database
# filling a database

import os
import MySQLdb


class DBHandler:
    __host = None
    __user = None
    __password = None
    __port = None

    __char_set = 'utf8'
    __collate = 'utf8_general_ci'

    __exclude_sql_parts = ['SET @@GLOBAL.GTID_PURGED='';']
    __mysql_global_vars = ['SET GLOBAL max_allowed_packet=268435456;']  # for admin
    __skip_dbs = []
    __skip_existing = True

    __existing_databases = []

    __debug = False

    def __init__(self, host, user, password, port,
                 skip_dbs, skip_existing, exclude_sql_parts, mysql_global_vars,
                 char_set, collate, debug):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__port = port
        self.__skip_existing = skip_existing

        if self.__skip_existing is True:
            self.__existing_databases = self.__getExisting()

        if skip_dbs is not None:
            self.__skip_dbs = self.__skip_dbs + skip_dbs

        if exclude_sql_parts is not None:
            self.__exclude_sql_parts = self.__exclude_sql_parts + exclude_sql_parts

        if mysql_global_vars is not None:
            self.__mysql_global_vars = self.__mysql_global_vars + mysql_global_vars

        self.__char_set = char_set
        self.__collate = collate

        self.__debug = debug

        self.__print('db handler initialized...')

    def __getExisting(self):

        self.__print('fetching existing schemas...')

        list_dbs_query = 'SHOW SCHEMAS;'
        conn = self.__getConnection()
        cur = conn.cursor()
        cur.execute(list_dbs_query)
        result = cur.fetchall()

        self.__print(str(len(result)) + ' schemas found...')

        dbs = []
        for r in result:
            dbs.append(r[0])

        return dbs

    def __getConnection(self, db=None):
        if db is not None:
            self.__print('connecting to ' + self.__host + ' ' + db + ' ...')
        else:
            self.__print('connecting to ' + self.__host)
        if db is not None:
            return MySQLdb.connect(host=self.__host,
                                   user=self.__user,
                                   passwd=self.__password,
                                   port=int(self.__port),
                                   db=db)
        else:
            return MySQLdb.connect(host=self.__host,
                                   user=self.__user,
                                   passwd=self.__password,
                                   port=int(self.__port))

    def __createDB(self, db_name):
        try:
            self.__print('creating db ' + db_name + ' ...')

            create_db_query = "CREATE DATABASE IF NOT EXISTS {db} CHARACTER SET {chs} COLLATE {cl};".format(
                db=db_name, chs=self.__char_set, cl=self.__collate)

            conn = self.__getConnection()
            cur = conn.cursor()
            cur.execute(create_db_query)
            conn.close()

            return True
        except Exception as e:
            # not created!
            return False

    def restoreMultiple(self, paths):
        for path in paths:
            db_name = self.__createDBName(path)
            if db_name in self.__skip_dbs:
                self.__print('skipping ' + db_name + ' because was set to be skip...')
                continue
            if db_name in self.__existing_databases:
                self.__print('skipping ' + db_name + ' because it already exists...')
                continue
            if self.__createDB(db_name):
                self.__restoreSingle(db_name, self.__get_content(path))

    def __restoreSingle(self, db_name, sql_content):

        self.__print('removing unnecessary content...')
        for pt in self.__exclude_sql_parts:
            sql_content = sql_content.replace(pt, "")

        # todo generalize this line
        sql_content = sql_content.encode('utf-8')
        try:
            self.__print('restoring ' + db_name + '...')

            conn = self.__getConnection(db_name)
            cursor = conn.cursor()
            cursor.execute(' '.join(self.__mysql_global_vars))
            cursor = conn.cursor()
            cursor.execute(sql_content)
            conn.close()
            return True
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            self.__print(e)
            return False

    def __get_content(self, path):
        self.__print('getting content from ' + path + '...')
        sql_content = ""
        with open(path, "r", encoding='utf-8') as fh:
            for line in fh:
                sql_content += line
                pass
        return sql_content

    def __createDBName(self, path):
        return os.path.basename(path).replace('.sql', '')

    def __print(self, msg):
        if self.__debug:
            print(msg)
