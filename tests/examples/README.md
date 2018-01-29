To generate those examples, follow this steps. 

First, start yout `mysql-server` with binlog enabled (ROW based), with the command: 

```mysql.server start --log-bin=binlog --binlog-format=ROW```.

Now, execute the following SQL in a already created database.

```sql
create table test_table
(
	column_1 int null,
	column_2 varchar(20) null
);

FLUSH LOGS;

START TRANSACTION;
INSERT INTO representante.test_table (column_1, column_2) VALUES (1, 'delete-me-1');
COMMIT;

START TRANSACTION;
DELETE FROM representante.test_table;
COMMIT;


START TRANSACTION;
INSERT INTO representante.test_table (column_1, column_2) VALUES (1, 'transaction-1');
INSERT INTO representante.test_table (column_1, column_2) VALUES (2, 'transaction-2');
UPDATE representante.test_table SET column_2 = 'updated';
COMMIT;

FLUSH LOGS;
SHOW BINARY LOGS; -- get the before last binlog
```

Now export the binlog with the extra parameters:

```
-- mysqlbinlog --base64-output=decode-rows -vv /usr/local/var/mysql/binlog.000016 > binlog-transaction-sample.txt
```
