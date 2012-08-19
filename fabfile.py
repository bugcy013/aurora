from os import path
from fabric.api import sudo, put, env, require, local
from fabric.decorators import with_settings
from time import gmtime, strftime

PROJECT_PATH = path.abspath(path.dirname(__file__))
# globals
env.project_name = 'aurora.local'
env.version = strftime("%Y%m%d%H%M", gmtime())


def prod():
    """
    Production config
    """
    env.user = 'deploy'  # have to be set up on server
    env.apache_user = 'www-data'  # default owner
    env.code_root_parent = '/web'
    env.hosts = ['axium@www.test-axium.com']
    env.release = env.version
    env.code_root = env.code_root_parent + '/' + env.project_name
    env.activate = 'source %s/bin/activate' % (env.code_root)
    env.whole_path = "%s/releases/%s/%s" % (env.code_root, env.release, env.project_name)
    env.whole_path_symlinked = "%s/releases/current/%s" % (env.code_root, env.project_name)
    env.ws_config_path = PROJECT_PATH + '/servers/prod/'
    env.branch = 'develop'


def setup_permissions():
    """
    Updates permissions on given project root
    """
    sudo('chown %s:%s -R %s' % (env.apache_user, env.apache_user, env.whole_path_symlinked))


@with_settings(warn_only=True)
def update_webserver_config():
    """
    Updates nginx and apache2 config.
    """
    require('ws_config_path', provided_by=[prod])
    apache_sa = '/etc/apache2/sites-available/'
    apache_se = '/etc/apache2/sites-enabled/'
    nginx_sa = '/etc/nginx/sites-available/'
    nginx_se = '/etc/nginx/sites-enabled/'

    sudo('rm %s%s' % (apache_sa, env.project_name))
    sudo('rm %s%s' % (apache_se, env.project_name))

    sudo('rm %s%s' % (nginx_sa, env.project_name))
    sudo('rm %s%s' % (nginx_se, env.project_name))

    put('%sapache2/sites-available/*' % (env.ws_config_path), apache_sa, use_sudo=True)
    put('%snginx/sites-available/*' % (env.ws_config_path), nginx_sa, use_sudo=True)

    sudo('ln -s %s%s %s' % (apache_sa, env.project_name, apache_se))
    sudo('ln -s %s%s %s' % (nginx_sa, env.project_name, nginx_se))
    restart_webservers()


def setup():
    """
    Setup a fresh virtualenv as well as a few useful directories, then run
    a full deployment
    """
    require('hosts', provided_by=[prod])
    require('code_root')
    sudo('apt-get update')
    sudo('apt-get install -y python-setuptools')
    sudo('easy_install pip')
    sudo('pip install virtualenv')
    sudo('aptitude install -y apache2')
    sudo('aptitude install -y libapache2-mod-wsgi')
    sudo('apt-get install -y nginx')
    update_webserver_config()
    sudo('mkdir -p %s; cd %s; virtualenv .;' % (env.code_root, env.code_root))
    sudo('cd %s;mkdir releases; mkdir shared; mkdir packages; mkdir shared/media; mkdir shared/media/file;' % (env.code_root))
    deploy()


def deploy():
    """
    Deploy the latest version of the site to the servers, install any
    required third party modules, then restart the webserver
    """
    require('hosts', provided_by=[prod])
    require('whole_path', provided_by=[prod])
    require('code_root')
    upload_tar_from_git(env.whole_path)
    install_requirements()
    symlink_current_release()
    migrate()
    restart_webservers()
    setup_permissions()


@with_settings(warn_only=True)
def upload_tar_from_git(path):
    """
    Create an archive from the current Git master branch and upload it
    """
    require('release', provided_by=[prod])
    require('whole_path', provided_by=[prod])
    require('branch', provided_by=[prod])
    local('git checkout %s' % (env.branch))
    local('git archive --format=tar %s | gzip > %s.tar.gz' % (env.branch, env.release))
    sudo('mkdir -p %s' % (path))
    put('%s.tar.gz' % (env.release), '/tmp/', mode=0755)
    sudo('mv /tmp/%s.tar.gz %s/packages/' % (env.release, env.code_root))
    sudo('cd %s && tar zxf ../../../packages/%s.tar.gz' % (env.whole_path, env.release))
    local('rm %s.tar.gz' % (env.release))
    sudo('rm %s/packages/%s.tar.gz' % (env.code_root, env.release))


def install_requirements():
    "Install the required packages from the requirements file using pip"
    require('whole_path', provided_by=[prod])
    sudo(env.activate)
    sudo('pip install -r %s/requirements.txt' % (env.whole_path))


@with_settings(warn_only=True)
def symlink_current_release():
    "Symlink current release"
    require('release', provided_by=[prod])
    sudo('cd %s/releases;rm current; ln -s %s current;' % (env.code_root, env.release))
    sudo('cd %s/media; ln -s %s/shared/media/file;' % (env.whole_path_symlinked, env.code_root))


def restart_webservers():
    "Restart the web servers"
    sudo('/etc/init.d/apache2 restart')
    sudo('/etc/init.d/nginx restart')


def migrate():
    "Update the database--Need to be fixed"
    require('project_name')
    sudo(env.activate)
    sudo('cd %s' % env.whole_path_symlinked + '/aurora; python manage.py syncdb; python manage.py migrate;')
