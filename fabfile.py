from __future__ import with_statement
from fabric.api import *

env.app = 'seahobo'
env.hosts = ['web2']
env.sites_dir = '/opt/sites/'
env.app_dir = env.sites_dir + env.app
env.repo = "https://github.com/reinbach/seahobo.git"
env.nginx_conf_dir = "/opt/nginx/conf/sites/"
env.uwsgi_conf_dir = "/etc/uwsgi/apps/"

def install():
    """Installs app on server"""
    with settings(user="root"):
        run("virtualenv --distribute --no-site-packages -p python2 {app_dir}".format(
            app_dir=env.app_dir
        ))
        with cd(env.app_dir):
            # clone repo
            run("git clone {repo} master".format(repo=env.repo))
            with cd("master"):
                run("source {app_dir}/bin/activate && python setup.py install".format(
                    app_dir=env.app_dir
                ))
                run("cp {app_dir}/master/nginx.conf {nginx_conf_dir}{app}.conf".format(
                    app_dir=env.app_dir,
                    nginx_conf_dir=env.nginx_conf_dir,
                    app=env.app
                ))
                run("cp {app_dir}/master/uwsgi.ini {uwsgi_conf_dir}{app}.ini".format(
                    app_dir=env.app_dir,
                    uwsgi_conf_dir=env.uwsgi_conf_dir,
                    app=env.app
                ))
                with cd("{app}".format(app=env.app)):
                    with cd("settings"):
                        run("rm -f currentenv.py")
                        run("ln -s prod.py currentenv.py")
                    # run("source {app_dir}/bin/activate && python manage.py syncdb".format(
                    #     app_dir=env.app_dir
                    # ))
                    # run("source {app_dir}/bin/activate && python manage.py migrate".format(
                    #     app_dir=env.app_dir
                    # ))
                    run('source {app_dir}/bin/activate && python manage.py collectstatic -v0 --noinput'.format(
                        app_dir=env.app_dir
                    ))
        run("systemctl reload uwsgi")
        run("systemctl reload nginx")

def update():
    """Updates code base on server"""
    with settings(user="root"):
        with cd("{app_dir}/master".format(app_dir=env.app_dir)):
            run("git pull")
            run("source {app_dir}/bin/activate && python setup.py install".format(
                app_dir=env.app_dir
            ))
            run("cp {app_dir}/master/nginx.conf {nginx_conf_dir}{app}.conf".format(
                app_dir=env.app_dir,
                nginx_conf_dir=env.nginx_conf_dir,
                app=env.app
            ))
            run("cp {app_dir}/master/uwsgi.ini {uwsgi_conf_dir}{app}.ini".format(
                app_dir=env.app_dir,
                uwsgi_conf_dir=env.uwsgi_conf_dir,
                app=env.app
            ))
            with cd("{app}".format(app=env.app)):
                # run("source {app_dir}/bin/activate && python manage.py syncdb".format(
                #     app_dir=env.app_dir
                # ))
                # run("source {app_dir}/bin/activate && python manage.py migrate".format(
                #     app_dir=env.app_dir
                # ))
                run('source {app_dir}/bin/activate && python manage.py collectstatic -v0 --noinput'.format(
                    app_dir=env.app_dir
                ))
        run("systemctl reload uwsgi")
        run("systemctl reload nginx")
