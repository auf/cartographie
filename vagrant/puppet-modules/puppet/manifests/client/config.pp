class puppet::client::config (
  $enable,
  $runinterval,
  $environment,
  $certname,
  $server,
  $masterport,
  $report,
  $kick,
  $kick_from,
  $splay,
  $splaylimit,
  $logfacility,
  $configtimeout,
  $etckeeperactive,
) {

  file { $puppet::variables::default_config_path:
    ensure  => file,
    content => template( "puppet/${::osfamily}/puppet_defaults.erb" ),
  }

  #This allows nagios to traverse the folder to check the status of Puppet agent
  file { '/var/lib/puppet':
    ensure => 'directory',
    owner  => 'puppet',
    group  => 'puppet',
    mode   => '0751',
  }

  if ( $etckeeperactive ) {
    package { 'etckeeper':
      ensure => installed,
    }
    $etckeeper_HPM = $puppet::variables::etckeeper_HPM
    $etckeeper_LPM = $puppet::variables::etckeeper_LPM
    file { 'etckeeper.conf':
      path    => $puppet::variables::etckeeper_config_path,
      content => template( 'puppet/etckeeper.conf.erb' ),
    }
  }

  concat::fragment { 'client_puppet.conf':
    order   => 05,
    target  => $puppet::variables::config_path,
    content => template( 'puppet/puppet_client.conf.erb' ),
  }

  if $kick {
    concat::fragment { 'auth_kick':
      order   => 50,
      target  => $puppet::variables::auth_config_path,
      content => template( 'puppet/auth_kick.conf.erb' ),
    }
  }
}
