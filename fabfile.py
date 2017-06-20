from fabric.api import (
    cd,
    env,
    local,
    put,
    run,
    sudo,
    task
)


HOME_DIRECTORY = '/home/ubuntu/'
INTAGE_DASHBOARD_PRODUCTION = 'ubuntu@34.211.236.143'


@task
def production():
    env.hosts = [
        INTAGE_DASHBOARD_PRODUCTION
    ]


def create_project_folder():
    run('mkdir -p intage-dash')


@task
def build_app():
    command = 'docker build -t intage-dash:live -f compose/django/Dockerfile-production .'
    local(command)

    command = 'docker tag intage-dash:live zkan/intage-dash'
    local(command)

    command = 'docker push zkan/intage-dash'
    local(command)


@task
def build_nginx():
    command = 'docker build -t intage-dash-nginx:live -f compose/nginx/Dockerfile compose/nginx'
    local(command)

    command = 'docker tag intage-dash-nginx:live zkan/intage-dash-nginx'
    local(command)

    command = 'docker push zkan/intage-dash-nginx'
    local(command)


@task
def deploy():
    create_project_folder()

    command = 'docker login'
    sudo(command)

    with cd('~/intage-dash'):
        put(
            'docker-compose.production.yml',
            '~/intage-dash/docker-compose.production.yml'
        )

        command = 'docker pull zkan/intage-dash'
        sudo(command)

        command = 'docker pull zkan/intage-dash-nginx'
        sudo(command)

        command = 'docker-compose -f docker-compose.production.yml up -d'
        sudo(command)
