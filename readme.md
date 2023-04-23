# Resurrector
Resurrector helps to restore your backed-up MySQL Databases to any specified instance.

## Support

<a href="https://www.buymeacoffee.com/rexshijaku" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="50" width="180"></a>

##### Pip
You can install this package from pip by running the following command :
```html
pip install resurrector
```

#### Pros

- Restore multiple databases at once
- No need o know CLI commands to treat backup files
- No need to know an OS to handle this process
- You can specify which databases should be restored and exclude those which should not.
- You can restore only missing databases in the instance (no need to treat the existing ones)

#### Good to know
Depending on your MySQL instance settings (such as user permissions or global variable specifications) you may need
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
backed up in your servers either automatically or manually. After connecting to the given database instance it creates these databases and "fills" them one by one (executes the whole .sql file (query) on their respective databases).

### Simple usage

```python

import resurrector

resurrector.resurrect(source='files/2022-07-06',
                      host='localhost',
                      user='root',
                      password='',
                      port=3306, skip_existing=True, debug=True)

```

### Contributions 
Feel free to contribute on development, testing or eventual bug reporting.

### Support
For general questions about the Resurrector, tweet at @rexshijaku or write me an email on rexhepshijaku@gmail.com.

### Author
##### Rexhep Shijaku
 - Email : rexhepshijaku@gmail.com
 - Twitter : https://twitter.com/rexshijaku

### License
MIT License

Copyright (c) 2022 | Rexhep Shijaku

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
