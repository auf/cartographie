class shinken::client::mdraid (
  $fqdn              = $::fqdn,
  $hostname          = $::hostname,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All,LocalChecks',
  $business_critical = true,
  $poller_tag        = 'Main'
){
  @@nagios_service { "mdraid_${fqdn}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => "check_nrpe!check_md_raid",
    service_description => 'Local raid check with mdstat',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}
