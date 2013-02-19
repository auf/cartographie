  include concat::setup
  include shinken::variables
  include shinken::install
  include shinken::server
  class { 'shinken::config':
    monitored_environments   => ['development','myevent'],
    extraconfigfile          => 'extrahosts.cfg',
    extraconfigfilesourceurl => "puppet:///${environment}/extrahosts.cfg",
  }
  include shinken::config::notificationcommands
  include shinken::config::commands
  include shinken::config::hostgroups
  include shinken::config::servicegroups
  include shinken::config::timeperiods
  include shinken::config::contactgroups
  class{ 'shinken::config::contacts':
    admin_email => 'stephane.duchesneau@savoirfairelinux.com',
    admin_paget => 'stephane.duchesneau@savoirfairelinux.com'
  }
  

  shinken::arbiter   { 'Arbiter 1':   }
  shinken::scheduler { 'Scheduler 1': }
  shinken::poller    { 'Poller 1':    }
  shinken::realm     { 'Main':
    isdefault => 1
  }
  
  nagios_realm { 'Toto':
    ensure => present
  }
}

