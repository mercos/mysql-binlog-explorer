# mysql-binlog-explorer

MySQL binlogs are the foundation for replication, but them can be useful for tracking intense write operations on database when using `binlog_format=ROW`. With that we can see all the changes that are actually applied to the database. For example: a statement like `delete from table where timestamp > ?` could affect just 3 or 1 million rows. Besides that, sometimes we have tons of very fast statements, but when composed together in a transaction it can takes lots of time.

This application aims to aid in tracking which transactions are being too write intensves.

## Usage (simplified)

```
pip install mysql-binlog-explorer
mysql-binlog-explorer ~/logs/mysql-bin-changelog.411078 --tenant-identifier company_id  --schema-ddl schema/my_db.ddl
```

We have two not required parameters (but they are quite useful).

- `schema-ddl` is a file with the DDL instructions to create the database. It'll be use used to show the column names in the statements. 
- `tenant-identifier` the name of a column which is used to store the tenant id (usually a column name that repeats across every table). This will aid in the generated charts.

## Usage (the real deal)

- Enable binlog (configuration varies depending on environment)
- Enable row format for binlog: `binlog_format=ROW`
- This kind o change needs to restart the server so **be careful**

Given that you already have a local mysql installation with `brew`, doing the above steps would mean:

```
mysql.server start --log-bin=binlog --binlog-format=ROW
```

Now you need the actual logs. In a MySQL session do the following:

```sql
SHOW BINARY LOGS; -- get the name of the binary log that you want to check
``` 

Now download it:

```
mysqlbinlog -h <HOST> -u <USER> -p<PASSWORD> --read-from-remote-server --base64-output=decode-rows -vv <NAME_FROM_STATEMENT_ABOVE> > my-bin-log.txt
```

**Don't forget the** `--base64-output=decode-rows -vv`, it's mandatory for the parser to work!

Now just use it.

```
mysql-binlog-explorer my-bin-log.txt
```

## Screenshot

![image](https://user-images.githubusercontent.com/771129/42182816-e111d4ce-7e15-11e8-8965-75847e7d4f02.png)

When the tenant information is used, the app can plot a chart with transactions/changes distribution per tenant identifier.

## Caveats

- Tested only with MySQL 5.6 binlogs, other versions may not work as expected.
- The result of the parsing is stored entirely in-memory, so it may crash for very large file sets.
