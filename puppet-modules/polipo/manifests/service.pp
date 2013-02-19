class polipo::service {
  service { 'polipo':
    ensure      => running,
    hasrestart => true,
    subscribe   => Class['polipo::config'],
    require     => Class['polipo::install'],
  }
}
