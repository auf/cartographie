class puppet::master::service (
  $ensure = running,
  $enable = true
  ) {
  service { 'puppetmaster':
    ensure    => $ensure,
    enable    => $enable,
    hasstatus => true,
  }
}
