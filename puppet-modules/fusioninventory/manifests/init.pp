# = Class: fusioninventory::common
#
# * Installs the fusioninventory package
#
# === Parameters:
#
# None.
# Class: fusioninventory::common
# install fusioninventory package

class fusioninventory::common {

  case $::osfamily {
    RedHat: {
      if  $operatingsystem != 'Fedora' {
        package { 'epel-release':
          ensure => present,
        }
        package { 'fusioninventory-agent': 
          ensure  => present,
          require => Package[epel-release]
        }
      } else {
        package { 'perl-LWP-Protocol-https': 
          ensure  => present,
        }
        package { 'fusioninventory-agent': 
          ensure  => present,
        }
      }
    }
    Debian: {
      package { 'libio-socket-ssl-perl': 
        ensure  => present,
      }
      include apt::repository::fusioninventory
      package { 'fusioninventory-agent': 
        ensure  => present,
        require => Class["apt::repository::fusioninventory"]
      }
    }
    default: { fail("Not available on this OS") }
  }

}

# = Class: fusioninventory::client
#
# * Configures fusioninventory as a client to glpi.savoirfairelinux.net
#
# === Parameters:
#
#
class fusioninventory::client inherits fusioninventory::common {
    file { "/etc/fusioninventory/agent.cfg" :
                ensure  => file,
                group   => root,
                owner   => root,
                source  => 'puppet:///modules/fusioninventory/agent.cfg',
                require => Package['fusioninventory-agent'],
        }
    $random_number = fqdn_rand(4,10)+8 # inventory on Tuesday Morning between 8AM and 12AM
    cron { fusioninventory:
        command   => "/usr/bin/fusioninventory-agent > /tmp/cron-fusinv.log 2>&1",
        user      => root,
        weekday   => 2,
        hour      => $random_number,
        minute    => 0
    }
}
