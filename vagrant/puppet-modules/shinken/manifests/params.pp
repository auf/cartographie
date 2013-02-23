class shinken::params {
  if $osfamily == 'RedHat' {
    $nrpe_package = 'nrpe'
    $nrpe_service = 'nrpe'
    $nrpe_has_status = true
  } elsif $osfamily == 'Debian' {
    $nrpe_package = 'nagios-nrpe-server'
    $nrpe_service = 'nagios-nrpe-server'
    $nrpe_has_status = false
  }
}
