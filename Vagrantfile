# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
	sudo apt-get update
	sudo apt-get install -y python-dev python-pip
	sudo apt-get install -y mongodb
	sudo apt-get install -y git unzip
	sudo pip install virtualenv
	sudo pip install virtualenvwrapper

	echo "export WORKON_HOME=/home/vagrant/.virtualenvs" >> /home/vagrant/.bashrc
	echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc

	export WORKON_HOME=/home/vagrant/.virtualenvs

	source /usr/local/bin/virtualenvwrapper.sh

	echo "Setting up dev environent"
	mkvirtualenv gae

	/home/vagrant/.virtualenvs/gae/bin/pip install -r /vagrant/requirements.txt
	/home/vagrant/.virtualenvs/gae/bin/pip install -r /vagrant/requirements-dev.txt

	wget https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.17.zip
	unzip google_appengine_1.9.17.zip

	echo "Setting up sqla example environent"
	mkvirtualenv sqla

	/home/vagrant/.virtualenvs/sqla/bin/pip install -r /vagrant/example/sqla/requirements.txt

	echo "Setting up mongodb example environent"
	mkvirtualenv mongodb

	/home/vagrant/.virtualenvs/mongodb/bin/pip install -r /vagrant/example/mongodb/requirements.txt

	chown -R vagrant:vagrant /home/vagrant/.virtualenvs

SCRIPT

Vagrant.configure(2) do |config|
    config.vm.box = "ubuntu/trusty64"
    config.vm.provision "shell", inline: $script
    config.vm.network "private_network", ip: "192.168.113.4"
    config.vm.network "forwarded_port", host_ip: "127.0.0.1", host: 5055, guest: 5055
    config.vm.synced_folder "example/gae/lib", "/vagrant/example/gae/lib", disabled: true
    config.vm.provider "virtualbox" do |v|
        v.memory = 1024
        v.cpus = 2
    end
end
