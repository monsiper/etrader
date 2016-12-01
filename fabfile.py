from fabric.api import run, local

# ssh myserver -c './manage.py collectstatic' -> run
# ./mange.py collectatic -> run


def test_and_run():

    # run('./manage.py collectstatic')
    start_postgres()
    local('pip install -q -r requirements.txt')
#    local('./manage.py test')
    local('./manage.py runserver 0.0.0.0:12345')


def freeze_requirements():
    local('pip freeze > requirements.txt')


def start_postgres():
    local('pg_ctl start -D "/Users/monsiper/Library/Application Support/Postgres/var-9.5" &')

def stop_postgres():
    local('pg_ctl stop -D "/Users/monsiper/Library/Application Support/Postgres/var-9.5"')