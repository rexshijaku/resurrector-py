import gzip
import shutil
import tempfile
import zipfile
from pathlib import Path
from distutils.dir_util import copy_tree


class BackupHandler:
    source_file_path = ''
    db_handler = None

    __debug = False

    def __init__(self, source_file_path, debug=False):
        self.source_file_path = source_file_path
        self.__debug = debug

    def __unzip_all_gz2sql(self, path):
        # unzip all .gz files to sql files
        self.__print('unzipping ' + str(path))

        for gz_file in Path(path).rglob('*.gz'):
            gz_file_path = Path(gz_file).absolute()
            self.__gunzip_shutil(gz_file, str(gz_file_path).replace('.gz', '.sql'))

    def __gunzip_shutil(self, source_filepath, destination_filepath, block_size=65536):
        # unzip a given source file
        self.__print('unzipping ' + str(source_filepath))

        with gzip.open(source_filepath, 'rb') as s_file, \
                open(destination_filepath, 'wb') as d_file:
            shutil.copyfileobj(s_file, d_file, block_size)

    # handle the given folder or zip file
    def resolve(self):
        self.__print('resolving the backup file...')

        temp_dir = tempfile.mkdtemp()
        sql_files_array = []

        if self.source_file_path.endswith('.zip'):
            zf = zipfile.ZipFile(self.source_file_path)
            zf.extractall(temp_dir)
        else:
            copy_tree(self.source_file_path, temp_dir)

        self.__unzip_all_gz2sql(temp_dir)
        for file in Path(temp_dir).rglob('*.sql'):
            sql_files_array.append(str(file))

        return temp_dir, sql_files_array

    def __print(self, msg):
        if self.__debug:
            print(msg)
