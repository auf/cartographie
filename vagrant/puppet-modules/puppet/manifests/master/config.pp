class puppet::master::config (
  $dnsaltnames,
  $puppetmaster_external_node,
  $puppetmaster_external_node_script,
  $puppet_db_server,
  $puppet_db_port,
  $reports,
  $reporturl,
  $autosign
  ) {

  file { '/etc/puppet/files':
    ensure  => directory,
    owner   => 'puppet',
    group   => 'puppet',
  }

  concat::fragment { 'master_puppet.conf':
    order   => 10,
    target  => '/etc/puppet/puppet.conf',
    content => template('puppet/puppet_master.conf.erb'),
  }

  concat::fragment { 'auth_master':
    order   => 10,
    target  => $puppet::variables::auth_config_path,
    content => template( 'puppet/auth_master.conf.erb' ),
  }

  file { '/etc/puppet/puppetdb.conf':
    ensure  => file,
    content => template('puppet/puppetdb.conf.erb'),
  }
}
