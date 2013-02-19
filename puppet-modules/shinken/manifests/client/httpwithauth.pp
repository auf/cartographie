define shinken::client::httpwithauth (
  $fqdn              = $::fqdn,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All',
  $business_critical = true,
  $poller_tag        = 'Main',
){
  @@nagios_service { "website_${name}_${path}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => "check_http_with_auth!${name}",
    service_description => "website_${name} has auth security",
    use        => $business_critical ? { 
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}

