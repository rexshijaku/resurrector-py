# Resurrector
Resurrector helps you to restore your backed-up MySQL Databases to any specified instance.

##### Pip
You can install this package from pip by running the following command :
```html
pip install resurrector
```

#### Pros

- Restore multiple databases at once
- No need o know CLI commands to treat backup files
- No need to know an OS to handle this process
- You can specify which databases should be restored and exclude dbs which are should not.
- You can restore only missing databases in the instance (no need to treat the existing ones)
- Automatic decompression

#### Good to know
Depending on your MySql instance settings (such as user permissions or global variable specifications) you may need
to deal with input parameters of the Ressurector (see below).

#### Parameters

Name | Description | Type | Default
--- | --- | --- | --- 
source | Input Folder (.zip or just normal folder) | string | -
host | MySQL Instance Ip | string | localhost
user | MySQL Instance User | string | root
port | MySQL Instance Port | integer | 3306
skip_dbs | List of Databases to skip | array | None
skip_existing | Should it skip the existing Databases? | boolean | True
mysql_global_vars | Global variables which should be run before each restoration | string (if multiple then semicolon sepearated) | SET @@GLOBAL.GTID_PURGED='';
exclude_sql_parts | SQL contents which should be removed | string | SET GLOBAL max_allowed_packet=268435456;
charset | Database charset | string | utf8
collate | Database collation | string | utf8_general_ci
debug | Debug the process on console | boolean | False



### How it works
Resurrector reads a folder (either as zipped or not) and searches for .gz files in it, these must contain .sql files which were
backed up in your servers either automatically or manually. After connecting to the given database instance it creates these databases by
and "fills" them one by one (executes the whole .sql file (query) on each respective database).

### Simple usage

```python

import resurrector

resurrector.resurrect(source='files/2022-07-06',
                      host='localhost',
                      user='root',
                      password='',
                      port=3306, skip_existing=True, debug=True)

```