# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
	sudo apt-get update
	sudo apt-get install -y python-dev python-pip
	sudo apt-get install -y mongodb
	sudo pip install virtualenv
	sudo pip install virtualenvwrapper

	echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
	echo "export PROJECT_HOME=/vagrant/example/" >> ~/.bashrc
	echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc

	source /usr/local/bin/virtualenvwrapper.sh

	mkvirtualenv dev
	mkvirtualenv sqla
	mkvirtualenv mongodb
SCRIPT
Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provision "shell", inline: $script
  config.vm.network "private_network", ip: "192.168.113.4"
end
