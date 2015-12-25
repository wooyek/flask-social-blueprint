# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
    # ======================================
    # System update and common utilities
    # ======================================

    cat /vagrant/.ssh_key >> .ssh/authorized_keys

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install -y htop git unzip
    sudo apt-get install -y build-essential libffi-dev libssl-dev
    sudo apt-get install -y python python-dev python-pip python-virtualenv
    sudo apt-get install -y mongodb
	sudo pip install virtualenvwrapper

    # Change Time Zone
    # dpkg-reconfigure tzdata
    sudo timedatectl set-timezone Europe/Warsaw

    # ======================================
    # Vagrant development setup
    # ======================================

	echo "export WORKON_HOME=/home/vagrant/.virtualenvs" >> /home/vagrant/.bashrc
	echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc
	export WORKON_HOME=/home/vagrant/.virtualenvs
	source /usr/local/bin/virtualenvwrapper.sh

    # ======================================
	echo "Setting up virtual environments"
	mkvirtualenv dev
	/home/vagrant/.virtualenvs/dev/bin/pip install -r /vagrant/requirements.txt
	/home/vagrant/.virtualenvs/dev/bin/pip install -r /vagrant/requirements-dev.txt

    # ======================================
	echo "Setting up sqla example environment"
	mkvirtualenv sqla
	/home/vagrant/.virtualenvs/sqla/bin/pip install -r /vagrant/example/sqla/requirements.txt

    # ======================================
	echo "Setting up mongodb example environment"
	mkvirtualenv mongodb
	/home/vagrant/.virtualenvs/mongodb/bin/pip install -r /vagrant/example/mongodb/requirements.txt

    # ======================================
	echo "Setting up gae example environment"
	mkvirtualenv gae
    /home/vagrant/.virtualenvs/gae/bin/pip install --target=/vagrant/example/gae/lib -r /vagrant/example/gae/requirements.txt
    wget https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.30.zip
	unzip google_appengine_1.9.30.zip

	chown -R vagrant:vagrant /home/vagrant/.virtualenvs

SCRIPT

Vagrant.configure(2) do |config|
    config.vm.box = "ubuntu/trusty64"
    config.vm.hostname = "vagrant"
    config.vm.provision "shell", inline: $script
    config.vm.network "private_network", ip: "192.168.113.4"
    config.vm.network "forwarded_port", host_ip: "127.0.0.1", host: 5055, guest: 5055
    config.vm.synced_folder "example/gae/lib", "/vagrant/example/gae/lib", disabled: true
    config.vm.provider "virtualbox" do |v|
        v.memory = 1024
        v.cpus = 2
    end
end
