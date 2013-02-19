# only centos
class ntp::privateserver (
  $ntp_servers # list of internal ntp servers (Windows DC?)
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
    content => template('ntp/private.ntp.conf.erb'),
    notify => Service['ntpd'],
    require => Package['ntp']
  }
  file {'/etc/ntp/step-tickers':
    owner   => root,
    group => root,
    mode => 0644,
    content => template('ntp/step-tickers.erb'),
    notify => Service['ntpd'],
    require => Package['ntp']
  }
}

