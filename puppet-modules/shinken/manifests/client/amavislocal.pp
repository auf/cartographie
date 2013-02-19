class shinken::client::amavislocal (
  $fqdn              = $::fqdn,
  $hostname          = $::hostname,
  $warningdelay      = 4,
  $criticaldelay     = 8,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All,LocalChecks',
  $business_critical = true,
  $poller_tag        = 'Main'
){
  @@nagios_service { "amavislocal_${fqdn}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => "check_nrpe!check_smtp_amavis",
    service_description => 'Local amavis port 10024 checking',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}
