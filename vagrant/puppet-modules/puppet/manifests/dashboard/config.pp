class puppet::dashboard::config (
  $db_host,
  $db_port,
  $db_name,
  $db_user,
  $db_password,
  $ca_server,
  $ca_port,
  $inventory_server,
  $inventory_port,
  $enable_inventory,
  $read_only_mode,
  $reporting_cutoff,
  $time_zone,
  $manage_mysql,
) {

  file { '/etc/puppet-dashboard':
    ensure => directory,
    mode   => '0755'
  }
  file { '/etc/puppet-dashboard/database.yml':
    ensure  => file,
    owner   => $apache2::variables::apache_user,
    group   => $apache2::variables::apache_group,
    mode    => '0644',
    content => template('puppet/dashboard_database.yml.erb'),
  }
  file { '/etc/puppet-dashboard/settings.yml':
    ensure  => file,
    owner   => $apache2::variables::apache_user,
    group   => $apache2::variables::apache_group,
    content => template('puppet/dashboard_settings.yml.erb'),
  }
  file { '/usr/share/puppet-dashboard/log':
    ensure => link,
    target => '/var/log/puppet-dashboard',
    force  => true,
  }
  file { [ '/usr/share/puppet-dashboard/spool', '/var/log/puppet-dashboard' ]:
    ensure  => directory,
    owner   => $apache2::variables::apache_user,
    group   => $apache2::variables::apache_group,
  }
  file { '/etc/default/puppet-dashboard-workers':
    ensure  => file,
    content => template('puppet/dashboard_workers.erb'),
  }

  $require = $manage_mysql ? {
    true    => Database[$db_name],
    default => undef,
  }
  exec { 'init_puppet_dashboard_db':
    command => '/bin/sh -c \'cd /usr/share/puppet-dashboard && rake RAILS_ENV=production db:migrate\'',
    unless  => "mysql -u${db_user} -p${db_password} --host ${db_host} --port=${db_port} --protocol=tcp -D ${db_name} -e 'SHOW TABLES' | grep nodes",
    require => $require,
  }

  if $enable_inventory {
    exec { 'dashboard_create_key_pair':
      command => '/bin/sh -c \'cd /usr/share/puppet-dashboard && rake cert:create_key_pair\'',
      creates => '/usr/share/puppet-dashboard/certs/dashboard.private_key.pem',
    }

    # You still have to run
    # rake cert:request
    # rake cert:retrieve (once signed on the ca)

    file { '/usr/share/puppet-dashboard/certs':
      ensure  => directory,
      owner   => $apache2::variables::apache_user,
      group   => $apache2::variables::apache_group,
      recurse => true,
      require => Exec[ 'dashboard_create_key_pair' ],
    }
  }
}
