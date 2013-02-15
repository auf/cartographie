class puppet::db::service (
  $ensure = running,
  $enable = true
) {
  service { 'puppetdb':
    ensure    => $ensure,
    enable    => $enable,
    hasstatus => true,
  }
}
