class shinken::client::brother_toner_level(
  $fqdn              = $::fqdn,
  $hostname          = $::hostname,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All',
  $check_interval    = '60',
  $warn              = '21',
  $crit              = '11',
  $business_critical = false,
  $poller_tag        = 'Main'
){
  @@nagios_service { "brother_toner_level_${fqdn}":
    host_name           => $fqdn,
    check_interval      => $check_interval,
    check_command       => "check_nrpe!check_brother_toner_level!${warn}!${crit}",
    service_description => 'Check Brother Toner Level',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}
