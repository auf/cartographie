class shinken::client::ssh (
  $fqdn              = $::fqdn,
  $hostname          = $::hostname,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All',
  $poller_tag        = 'Main',
  $business_critical = true,
  $port              = '22'
){
  @@nagios_service { "ssh_${fqdn}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => "check_ssh!${port}",
    service_description => 'SSH connection',
    use        => $business_critical ? { 
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}
