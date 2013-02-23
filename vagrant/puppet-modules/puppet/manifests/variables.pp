class puppet::variables {
  case $::osfamily {
    /(?i-mx:debian)/ : {
      $default_config_path      = '/etc/default/puppet'
      $default_db_config_path   = '/etc/default/puppetdb'
      $puppetdb_conf_dir        = '/etc/puppetdb'
      $client_packages          = [ 'puppet', 'libaugeas-ruby' ]
      $etckeeper_LPM            = 'dpkg'
      $etckeeper_HPM            = 'apt'
    }
    /(?i-mx:redhat)/ : {
      $default_config_path      = '/etc/sysconfig/puppet'
      $default_db_config_path   = '/etc/sysconfig/puppetdb'
      $client_packages          = [ 'puppet', 'ruby-augeas' ]
      $etckeeper_LPM            = 'rpm'
      $etckeeper_HPM            = 'yum'
    }
    default : {
      fail('Unsupported operating system')
    }
  }
  $config_path           = '/etc/puppet/puppet.conf'
  $auth_config_path      = '/etc/puppet/auth.conf'
  $etckeeper_config_path = '/etc/etckeeper/etckeeper.conf'
}
