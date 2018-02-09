# mysql-binlog-explorer

MySQL binlogs are the foundation for replication, but them can be useful for tracking intense write operations on database when using `binlog_format=ROW`. With that we can see all the changes that are actually applied to the database. For example: a statement like `delete from table where timestamp > ?` could affect just 3 or 1 million rows. Besides that, sometimes we have tons of very fast statements, but when composed together in a transaction takes a lot of time.

This application aims to aid in tracking which transactions are being too write intensves.

## usage (simplified)

```
pip install mysql-binlog-explorer
mysql-binlog-explorer ~/logs/mysql-bin-changelog.411078
```

## usage (the real deal)

- Enable binlog (configuration varies depending on environment)
- Enable row format for binlog: `binlog_format=ROW`
- This kind o change needs to restart the server so **be careful**

In a local mysql installed with `brew` the above would be converted to:

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


## caveats

- Tested only with MySQL 5.6 binlogs, othere versions probably have different formats. Create a PR for new formats if you may so.
- The result of the parsing is stored entirely in-memory, so for very large file sets it may crash.
