class shinken::client::dns (
  $fqdn              = $::fqdn,
  $hostname          = $::hostname,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All',
  $poller_tag        = 'Main',
  $query             = $::domain,
  $business_critical = true
){
  @@nagios_service { "dns_${fqdn}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => "check_dns!${query}",
    service_description => 'Dns request',
    use        => $business_critical ? { 
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}
