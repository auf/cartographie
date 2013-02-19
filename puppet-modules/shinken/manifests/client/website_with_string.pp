define shinken::client::website_with_string (
  $fqdn              = $::fqdn,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All',
  $poller_tag        = 'Main',
  $path              = '/',
  $business_critical = true,
  $port              = 80,
  $expect_string,
  $website_name      = $name,
  $warn_time         = '5',
  $crit_time         = '10',
){
  @@nagios_service { "website_${website_name}_${path}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => "check_website!${warn_time}!${crit_time}!${website_name}!${path}!${port}!${expect_string}",
    service_description => "website_${website_name}",
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}

