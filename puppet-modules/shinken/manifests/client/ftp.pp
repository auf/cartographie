class shinken::client::ftp (
  $fqdn              = $::fqdn,
  $hostname          = $::hostname,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All',
  $poller_tag        = 'Main',
  $business_critical = true
){
  @@nagios_service { "ftp_${fqdn}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => 'check_ftp!5!10',
    service_description => 'Ftp',
    use        => $business_critical ? { 
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}
