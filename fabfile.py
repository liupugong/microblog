#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import datetime

####################
# deploy code
####################
from fabric.api import (
    env,
    execute,
    hosts,
    local,
    sudo,
    task,
    runs_once,
    lcd,
)

####################
# Env define
####################
env.use_ssh_config = True
env.keepalive = 60

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))

P_HOSTS = ['192.168.1.204']

env.hosts=['root@192.168.1.204',] #ssh要用到的参数


# platform
ROOT_DIR_V2 = os.path.dirname(os.path.abspath(__file__))
DEPLOY_DIR_V2 = "{}/".format(ROOT_DIR_V2)
REMOTE_VERSION_V2 = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
REMOTE_DIR_V2 = '/data/www/pydemo/{}'.format(REMOTE_VERSION_V2)
REMOTE_USER_V2 = 'www-data'
#  = 'rsync_exclude.txt'


####################
# Tasks Define
####################
@task
def fetch():
    local("ls -l")
    #local("git fetch")
    #local("svn **")
    print("todo: fetch the source code")

@task
def tag():
    local('git fetch origin --prune --tags')

    name = 'v{}'.format(datetime.datetime.now().strftime('%Y%m%d%H%M'))
    local('git tag -f {}'.format(name))
    local('git push --tags')


@task()
@runs_once
def build():
    with lcd(PROJECT_PATH):
        local('rm -rf ./build/')
        local('make html')
        # local('make pdf')


@task
def deploy():
    sudo("mkdir -p {}".format(REMOTE_DIR_V2))
    sudo("chown {0} -R {1}".format(env.user, REMOTE_DIR_V2))
    local(
        "rsync -az --progress --force --delete --delay-updates "
        "--exclude-from={0} {1}/ {3}:{2}/".format(
            ROOT_DIR_V2,
            DEPLOY_DIR_V2,
            REMOTE_DIR_V2,
            env.host_string,
        )
    )
    sudo("chown {0} -R {1}".format(REMOTE_USER_V2, REMOTE_DIR_V2))
    sudo("rm /var/www/data")
    sudo("ln -s {0} /var/www/data".format(REMOTE_DIR_V2))

@task
#@hosts(P_HOSTS)
def p_deploy():
    execute(fetch)
    execute(build)
    execute(deploy)
    print("deploy complete, don't forget to tag")
