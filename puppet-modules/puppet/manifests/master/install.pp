class puppet::master::install {
  package { [ 'puppetmaster', 'puppetdb-terminus' ]:
    ensure => present,
  }
}
