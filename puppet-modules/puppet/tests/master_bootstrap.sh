#!/bin/sh

ENV_BASE=/etc/puppet/environments
ENV_LIST='development production'
RELEASE=`lsb_release -c -s`

wget http://apt.puppetlabs.com/puppetlabs-release-$RELEASE.deb
dpkg -i puppetlabs-release-$RELEASE.deb
apt-get update

apt-get install facter
FQDN=`facter fqdn`
grep $FQDN /etc/hosts
if [ $? -eq 1 ];then
	echo "Please ensure that your FQDN is in  /etc/hosts"
	exit 1
else
	apt-get -y install puppet git
fi

mkdir -p $ENV_BASE/sharepoint/modules
cd $ENV_BASE/sharepoint/modules
git clone --bare git://github.com/ripienaar/puppet-concat.git concat
git clone --bare git://github.com/puppetlabs/puppetlabs-stdlib.git stdlib
git clone --bare git://github.com/cprice-puppet/puppetlabs-inifile.git inifile
git clone --bare gitosis@git.savoirfairelinux.com:puppet-module-sfl-packages packages
git clone --bare git@github.com:Unyonsys/puppet-module-apache2.git apache2
git clone --bare gitosis@git.savoirfairelinux.com:puppet-module-sfl-puppet puppet

for  ENV in $ENV_LIST
do
        cd $ENV_BASE
        mkdir $ENV_BASE/$ENV
        mkdir $ENV_BASE/$ENV/modules
        mkdir $ENV_BASE/$ENV/site
        mkdir $ENV_BASE/$ENV/hieradata

        cd $ENV_BASE/$ENV/modules
        for dir in `ls $ENV_BASE/sharepoint/modules`
        do
                git clone $ENV_BASE/sharepoint/modules/$dir $dir
        done
done

puppet apply --modulepath=/etc/puppet/environments/production/modules /etc/puppet/environments/production/modules/puppet/tests/server.pp
