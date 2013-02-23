class fail2ban (
  $ignoreip = []
) {
   
  package{'fail2ban': ensure => installed}
  service { 'fail2ban':
    ensure     => running,
    enable     => true,
    hasrestart => true,
    hasstatus  => true,
    require    => [ File['/etc/fail2ban/jail.conf'],
#                    File['jail.local'],
                    File['/etc/fail2ban/fail2ban.conf'],
                    Package['fail2ban'] ]
  }

  file {'/etc/fail2ban/fail2ban.conf':
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    source  => 'puppet:///fail2ban/fail2ban.conf',
    require => Package['fail2ban']
  }
                                    
  file {'/etc/fail2ban/jail.conf':
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    content => template("fail2ban/jail.conf.erb"),
    require => Package['fail2ban']
  }
}
