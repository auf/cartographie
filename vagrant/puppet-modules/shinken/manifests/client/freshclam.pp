class shinken::client::freshclam (
  $fqdn              = $::fqdn,
  $hostname          = $::hostname,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All,LocalChecks',
  $poller_tag        = 'Main',
  $business_critical = false
){
  @@nagios_service { "freshclam_${fqdn}":
    host_name           => $fqdn,
    check_interval      => '30',
    check_command       => 'check_nrpe!check_freshclam',
    service_description => 'Freshclam running',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}

