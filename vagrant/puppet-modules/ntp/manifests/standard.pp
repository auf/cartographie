# = Class: ntp::standard
#
# * Installs ntp daemon
class ntp::standard (
  $my_region ='europe'
) {
  package { 'ntp':
    ensure => present
  }
  service { 'ntpd':
      ensure          => running,
      enable          => true,
      hasstatus       => true,
      require         => Package['ntp'],
  }
  file {'/etc/ntp.conf':
    owner   => root,
    group => root,
    mode => 0644,
    content => template('ntp/ntp.conf.erb'),
    notify => Service['ntpd'],
    require => Package['ntp']
  }

}


