class shinken::client::postfix10025local (
  $fqdn              = $::fqdn,
  $hostname          = $::hostname,
  $warningdelay      = 4,
  $criticaldelay     = 8,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All,LocalChecks',
  $business_critical = true,
  $poller_tag        = 'Main'
){
  @@nagios_service { "postfix10025local_${fqdn}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => "check_nrpe!check_smtp_10025",
    service_description => 'Local postfix port 10025 checking',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}
