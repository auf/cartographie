class shinken::client::zombieprocs (
  $fqdn              = $::fqdn,
  $hostname          = $::hostname,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All,LocalChecks',
  $business_critical = true,
  $poller_tag        = 'Main'
){
  @@nagios_service { "zombieprocs_${fqdn}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => 'check_nrpe!check_zombie_procs',
    service_description => 'zombie procs',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
  if $osfamily == 'RedHat' {
    $nrpe_zombieprocs_file = '/etc/nrpe.d/zombieprocs.cfg'
  } 
  if $osfamily == 'Debian' {
    $nrpe_zombieprocs_file = '/etc/nagios/nrpe.d/zombieprocs.cfg'
  }

  file { "$nrpe_zombieprocs_file":
    ensure  => present,
    owner   => 'nagios',
    group   => 'nagios',
    mode    => 644,
    content => 'command[check_zombie_procs]=/usr/lib/nagios/plugins/check_procs -w 5 -c 10 -s Z',
  }

}
