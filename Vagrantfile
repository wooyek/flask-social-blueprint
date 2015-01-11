# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
	sudo apt-get update
	sudo apt-get install -y python-dev python-pip
	sudo apt-get install -y mongodb
	sudo apt-get install -y git
	sudo pip install virtualenv
	sudo pip install virtualenvwrapper

	echo "export WORKON_HOME=/home/vagrant/.virtualenvs" >> /home/vagrant/.bashrc
	echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc

	export WORKON_HOME=/home/vagrant/.virtualenvs

	source /usr/local/bin/virtualenvwrapper.sh

	echo "Setting up dev environent"
	mkvirtualenv dev

	/home/vagrant/.virtualenvs/dev/bin/pip install -r /vagrant/requirements.txt
	/home/vagrant/.virtualenvs/dev/bin/pip install -r /vagrant/requirements-dev.txt

	echo "Setting up sqla example environent"
	mkvirtualenv sqla

	/home/vagrant/.virtualenvs/sqla/bin/pip install -r /vagrant/example/sqla/requirements.txt
	/home/vagrant/.virtualenvs/sqla/bin/pip install -r /vagrant/example/sqla/requirements-dev.txt


	echo "Setting up mondodb example environent"
	mkvirtualenv mongodb

	/home/vagrant/.virtualenvs/mongodb/bin/pip install -r /vagrant/example/mongodb/requirements.txt

	chown -R vagrant:vagrant /home/vagrant/.virtualenvs

SCRIPT
Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provision "shell", inline: $script
  config.vm.network "private_network", ip: "192.168.113.4"
end
