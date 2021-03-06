
```commandline
virtualenv -p python3 venv
source venv/bin/activate

рекомендуется
sudo apt-get install python3.5-dev

pip3 install -r requirements.txt

```

## Create DB and user
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
```
## start gunicorn

конфиг Gunicorn из папки extra/systemd/gunicorn.service в /etc/systemd/system


```bash
systemctl daemon-reload
systemctl start gunicorn.service
systemctl status gunicorn.service
systemctl restart gunicorn.service

```

проверка
ps xa | grep gunicorn

#run celery worker

## manual start celery
celery worker -A ticker.celery_worker.celery --loglevel=info

or 
## start celery daemon

конфиг Celery из папки extra/systemd/celery.service в /etc/systemd/system
конфиг Celery из папки extra/systemd/celeryd в /etc/default

```bash
systemctl daemon-reload
systemctl start celery.service
systemctl status celery.service
systemctl restart celery.service

```

## crontab

Add line. 
```bash
*/5 * * * * /home/deployer/tickers/venv/bin/python3 /home/deployer/tickers/manage.py runtickers
```

# Restart all

```bash
sudo bash /home/deployer/ticker/restart.sh
```

## Usage
```html
/api/v1/data/price?pair=BTC:USD&ts=1513888428&market=2&format=string

`format` = `string` or `float`. Default value is `float`
```
all parameters are optional

### Version

```bash
python manage.py version
```
or 
```html
/api/version
```


