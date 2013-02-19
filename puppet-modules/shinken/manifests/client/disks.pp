class shinken::client::disks (
  $fqdn              = $::fqdn,
  $hostname          = $::hostname,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All,LocalChecks',
  $business_critical = true,
  $poller_tag        = 'Main',
){
  @@nagios_service { "Disks_${fqdn}":
    host_name           => $fqdn,
    check_command       => $::operatingsystem ? {
    'Fedora' => 'check_nrpe!check_disk_nofuse',
    default  => 'check_nrpe!check_disk',
    },
    service_description => 'Disks',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}
