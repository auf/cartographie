class shinken::client::dkimlocal (
  $fqdn              = $::fqdn,
  $hostname          = $::hostname,
  $warningdelay      = 4,
  $criticaldelay     = 8,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All,LocalChecks',
  $business_critical = true,
  $poller_tag        = 'Main'
){
  @@nagios_service { "dkimlocal_${fqdn}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => "check_nrpe!check_smtp_dkim",
    service_description => 'Local dkim port 10027 checking',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}
