class shinken::client::asterisk (
  $fqdn              = $::fqdn,
  $hostname          = $::hostname,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All',
  $business_critical = true,
  $contacts          = $business_critical ? { true => 'admin_email,admin_paget', false => 'admin_email', undef => 'admin_email' },
  $poller_tag        = 'Main'
){
  @@nagios_service { "asterisk_${fqdn}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => "check_nrpe!check_asterisk",
    service_description => 'Asterisk is running',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    contacts            => $contacts,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}
