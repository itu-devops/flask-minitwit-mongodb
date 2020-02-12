# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "generic/ubuntu1804"

  config.vm.network "private_network", type: "dhcp"

  # For two way synchronization you might want to try `type: "virtualbox"`
  config.vm.synced_folder ".", "/vagrant", type: "rsync"

  config.vm.define "dbserver", primary: true do |server|
    server.vm.network "private_network", ip: "192.168.20.2"
    # config.vm.network "forwarded_port", guest: 27017, host: 37017
    # config.vm.network "forwarded_port", guest: 28017, host: 38017
    server.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
    end
    server.vm.hostname = "dbserver"
    server.vm.provision "shell", privileged: false, inline: <<-SHELL
        echo "Installing MongoDB"
        wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
        echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
        sudo apt-get update
        sudo apt-get install -y mongodb-org

        sudo mkdir -p /data/db
        sudo sed -i '/  bindIp:/ s/127.0.0.1/0.0.0.0/' /etc/mongod.conf

        sudo systemctl start mongod
        mongorestore --gzip /vagrant/dump
    SHELL
  end

  config.vm.define "webserver", primary: true do |server|
    server.vm.network "private_network", ip: "192.168.20.3"
    # server.vm.network "forwarded_port", guest: 5000, host: 5000
    server.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
    end
    server.vm.hostname = "webserver"
    server.vm.provision "shell", privileged: false, inline: <<-SHELL
        export DB_IP="192.168.20.2"

        echo "Installing Anaconda..."
        sudo wget https://repo.anaconda.com/archive/Anaconda3-2019.07-Linux-x86_64.sh -O $HOME/Anaconda3-2019.07-Linux-x86_64.sh
    
        bash $HOME/Anaconda3-2019.07-Linux-x86_64.sh -b
        
        echo ". $HOME/.bashrc" >> $HOME/.bash_profile
        echo "export PATH=$HOME/anaconda3/bin:$PATH" >> $HOME/.bash_profile
        export PATH="$HOME/anaconda3/bin:$PATH"
        rm $HOME/Anaconda3-2019.07-Linux-x86_64.sh
        source $HOME/.bash_profile

        pip install Flask-PyMongo

        cp -r /vagrant/* $HOME
        nohup python minitwit.py > out.log 2>&1 &
        echo "================================================================="
        echo "=                            DONE                               ="
        echo "================================================================="
        echo "Navigate in your browser to:"
        echo "http://192.168.20.3:5000"
    SHELL
  end

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    sudo apt-get update
  SHELL
end