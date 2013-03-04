# = Class: ntp::openntp
#
# * Installs ntpd and configure servers based on location
#
# === Parameters:
#
# $my_region (eu):: The region we are in (eu, ca ...)
class ntp::openntpd (
  $my_region ='europe'
) {
  if $my_region == 'eu' { $my_region = 'europe' } #eu.pool.ntp.org does not exist anymore
  package { 'openntpd' :
    ensure => present,
  }

  file {'/etc/openntpd/ntpd.conf':
    content => template('ntp/openntpd.conf.erb'),
    ensure  => file,
    require => Package['openntpd'],
    notify  => Service['openntpd'],
    owner   => root,
    group => root,
    mode => 0644,
  }
  
  file {'/etc/default/openntpd':
    source  => 'puppet:///modules/ntp/default_openntpd',
    ensure  => file,
    owner   => root,
    group => root,
    mode => 0644,
  }

  service {
    openntpd:
      ensure          => running,
      enable          => true,
      hasstatus       => false,
      require         => Package['openntpd'],
      pattern         => 'ntpd',
  }
}


