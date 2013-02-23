define shinken::client::tcp (
  $fqdn              = $::fqdn,
  $hostname_check    = $::fqdn,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All',
  $port              = '80',
  $poller_tag        = 'Main',
  $business_critical = true
){

  @@nagios_service { "tcp_${fqdn}_${port}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => "check_tcp!${hostname_check}!${port}",
    service_description => "Tcp port ${port}",
    use        => $business_critical ? { 
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}

