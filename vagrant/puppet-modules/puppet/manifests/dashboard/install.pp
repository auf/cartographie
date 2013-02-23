class puppet::dashboard::install {
  package { 'puppet-dashboard' :
    ensure => present,
  }
}
