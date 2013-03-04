#!/bin/bash

PUPPET_FOLDER=/etc/puppet
STDLIB=2.2.1
. /etc/lsb-release
REPO=ssh://root@puppetmaster/etc/puppet/environments/development/modules/

wget http://apt.puppetlabs.com/puppetlabs-release-$DISTRIB_CODENAME.deb
sudo dpkg -i puppetlabs-release-$DISTRIB_CODENAME.deb

sudo apt-get update
sudo apt-get install -y --allow-unauthenticated puppet git-core

mkdir -p $PUPPET_FOLDER/environments/sharepoint/modules
mkdir -p $PUPPET_FOLDER/environments/development/modules
cd $PUPPET_FOLDER/environments/development/modules

git clone git://github.com/ripienaar/puppet-concat.git concat
git clone git://github.com/puppetlabs/puppetlabs-stdlib.git stdlib
for MODULE in apt packages mysql apache2 puppet
do
    git clone $REPO/$MODULE $MODULE
done

cd $PUPPET_FOLDER/environments/development/modules/stdlib
git checkout -b b$STDLIB v$STDLIB
cd ..
