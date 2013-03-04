#check_zombie_procs
#check_total_procs
class shinken::client::procs (
  $fqdn              = $::fqdn,
  $hostname          = $::hostname,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All',
  $business_critical = true,
  $poller_tag        = 'Main'
){
  @@nagios_service { "procs_zombie_${fqdn}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => "check_nrpe!check_zombie_procs",
    service_description => 'Zombie processess',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}

