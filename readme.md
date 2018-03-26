
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

#run celery worker

## manual start celery
celery worker -A ticker.celery_worker.celery --loglevel=info

or 
## start celery deamon

from
https://github.com/celery/celery/tree/master/extra/generic-init.d

```bash
 Скопировать celeryd в /etc/init.d/celeryd
$ sudo chmod 755 /etc/init.d/celeryd
$ sudo chown root:root /etc/init.d/celeryd

Скопировать конфигурационный файл в /etc/default/celeryd

Запуск
$ sudo /etc/init.d/celeryd start
Статус
$ sudo /etc/init.d/celeryd status
Остановка
$ sudo /etc/init.d/celeryd stop
```

## crontab

Add line. 
```bash
*/5 * * * * /home/deployer/tickers/venv/bin/python3 /home/deployer/tickers/manage.py runtickers
```


## Usage
```html
/api/v1/data/price?pair=BTC:USD&ts=1513888428&market=2
```
all parameters are optional
