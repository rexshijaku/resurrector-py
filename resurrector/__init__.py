import shutil
from os import path
from resurrector.db_handler import DBHandler
from resurrector.backup_resolver import BackupHandler


def resurrect(source, host='localhost', user='root', password='', port=3306, skip_dbs=None, skip_existing=True,
              mysql_global_vars=None,
              exclude_sql_parts=None,
              char_set='utf8', collate='utf8_general_ci', debug=False):
    tmp_dir = ''
    try:
        tmp_dir, sql_files = BackupHandler(source, debug=debug).resolve()
        db = DBHandler(host, user, password, port,
                       skip_dbs, skip_existing, mysql_global_vars, exclude_sql_parts,
                       char_set, collate, debug)
        db.restoreMultiple(sql_files)
    except Exception as e:
        print('Resurrector failed the resurrection of a database. Error | ', e)
    finally:
        if path.isdir(tmp_dir):
            shutil.rmtree(tmp_dir)
