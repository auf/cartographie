class shinken::client::mptraid (
  $fqdn              = $::fqdn,
  $hostname          = $::hostname,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All,LocalChecks',
  $business_critical = true,
  $poller_tag        = 'Main'
){
  @@nagios_service { "mptraid_${fqdn}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => "check_nrpe!check_mpt_raid",
    service_description => 'Local hard raid check with mptstatus',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}
