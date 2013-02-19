class shinken::client::cpu (
  $fqdn              = $::fqdn,
  $hostname          = $::hostname,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All,LocalChecks',
  $business_critical = false,
  $poller_tag        = 'Main'
){
  @@nagios_service { "cpu_${fqdn}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => "check_nrpe!check_cpu",
    service_description => 'CPU',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}
