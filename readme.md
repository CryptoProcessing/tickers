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
## start gunicorn
если еще не установлен supervisor то
```bash
apt-get install supervisor
```

скопровать в /etc/supervisor/conf.d/
конфиг Gunicorn из папки extra/etc/supervisor/conf.d/tickers.conf

команды для supervisor
```bash
supervisorctl reread
supervisorctl update
supervisorctl status tickers
supervisorctl restart tickers
```
проверка
ps xa | grep gunicorn

```

## Usage
```html
/api/v1/data/pricelast?pair=BTC:USD&ts=1513888428
```
parameters are optional
