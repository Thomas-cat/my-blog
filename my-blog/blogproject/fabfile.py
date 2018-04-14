from fabric.api import env,run
from fabric.operations import sudo 

GIT_REPO = 'https://github.com/Thomas-cat/my-blog.git'
env.user = 'root'
env.password = 'Kangta123'
env.hosts = ['www.cckuzai.com']
env.port = '22'

def deploy():
	source_folder = '/root/sites/www.cckuza.com/my-blog' ③
	run('cd %s && git pull' % source_folder) ④
	run("""
	cd {} &&
	/usr/local/bin/python3 manage.py collectstatic --noinput &&
	/usr/local/bin/python3 manage.py migrate
	""".format(source_folder)) ⑤ 
	sudo('systemctl cckuzai restart') ⑥
	sudo('service nginx reload')
