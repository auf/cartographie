class shinken::client::mptraid::requirements {
  package { "mpt-status": 
    ensure => present, 
  }
  exec { "modprobe mptctl": 
    unless  => 'lsmod |grep -q mptctl',
    require => Package['mpt-status'],
  }
  file { "/dev/mptctl":
    mode    => '0660',
    group   => "nagios",
    require => Exec['modprobe mptctl']
  }
}
