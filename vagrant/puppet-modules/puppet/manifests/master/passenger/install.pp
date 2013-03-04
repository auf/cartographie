class puppet::master::passenger::install {
  package { 'puppetmaster-passenger':
    ensure  => present,
    require => Class['puppet::master::service'],
  }
  file { '/etc/apache2/sites-enabled/puppetmaster':
    ensure  => absent,
    require => Package[ 'puppetmaster-passenger' ],
  }
}
