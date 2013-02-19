class shinken::client::libvirt (
  $fqdn              = $::fqdn,
  $hostname          = $::hostname,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All',
  $check_interval    = '3600',
  $warn              = '90',
  $crit              = '95',
  $business_critical = false,
  $poller_tag        = 'Main',
  $uri               = "qemu+ssh://vmreport@$hostname/system",
  $unit              = 'GB',
){
  @@nagios_service { "libvirt_stat_${fqdn}":
    host_name           => $fqdn,
    check_interval      => $check_interval,
    check_command       => "check_libvirt_stats!${uri}!${unit}!${warn}!${crit}",
    service_description => 'Check memory and disk used on hypervisor',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}
