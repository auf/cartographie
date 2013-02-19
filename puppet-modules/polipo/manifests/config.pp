class polipo::config {
  file { '/etc/polipo/config':
    ensure => present,
    owner  => 'root',
    mode   => '644',
  }
}
