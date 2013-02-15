class puppet::client::service (
  $ensure,
  $enable,
) {
  service { 'puppet':
    ensure     => $ensure,
    enable     => $enable,
    hasstatus  => true,
    hasrestart => true,
  }
}
