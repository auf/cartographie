class shinken::client::clamd (
  $fqdn              = $::fqdn,
  $hostname          = $::hostname,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All,LocalChecks',
  $poller_tag        = 'Main',
  $business_critical = true
){
  @@nagios_service { "clamd_${fqdn}":
    host_name           => $fqdn,
    check_interval      => '10',
    check_command       => 'check_nrpe!check_clamd',
    service_description => 'ClamAV daemon running',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}

