Create DB and user
```bash
mysql -u root -p
```

```mysql
CREATE DATABASE tickers;
```
For tests
```mysql
CREATE DATABASE tickers_test;
```

```mysql
GRANT ALL ON tickers.* TO tickers@localhost IDENTIFIED BY 'tickers';
```

```mysql
GRANT ALL ON tickers_test.* TO tickers@localhost IDENTIFIED BY 'tickers';
```


## Миграции

только один раз
```bash
python manage.py db init
```

при каждом изменении
```bash
python manage.py db migrate
python manage.py db upgrade
```
## run celery worker
```bash
celery -A ticker worker --loglevel=info
```