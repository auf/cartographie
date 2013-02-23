class puppet::db::config (
  $java_args,
  $host,
  $ssl_host,
) {

  file { $puppet::variables::default_db_config_path:
    ensure  => file,
    content => template('puppet/puppetdb_defaults.erb'),
  }

  exec { 'puppetdb_ssl_setup':
    command => '/usr/sbin/puppetdb-ssl-setup',
    creates => "${puppet::variables::puppetdb_conf_dir}/ssl/puppetdb_keystore_pw.txt",
  }

  ini_setting { 'jetty_host':
    path    => "${puppet::variables::puppetdb_conf_dir}/conf.d/jetty.ini",
    section => 'jetty',
    setting => 'host',
    value   => $host,
    ensure  => present,
  }
  ini_setting { 'jetty_ssl_host':
    path    => "${puppet::variables::puppetdb_conf_dir}/conf.d/jetty.ini",
    section => 'jetty',
    setting => 'ssl-host',
    value   => $ssl_host,
    ensure  => present,
  }
}
