class puppet::dashboard::service {
  service { 'puppet-dashboard-workers':
    ensure    => running,
    enable    => true,
    hasstatus => true,
  }
}