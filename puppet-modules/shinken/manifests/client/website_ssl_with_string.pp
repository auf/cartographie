define shinken::client::website_ssl_with_string (
  $expect_string,
  $fqdn              = $::fqdn,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All',
  $poller_tag        = 'Main',
  $path              = '/',
  $business_critical = true,
  $port              = 80,
  $website_name      = $name,
  $warn_time         = '5',
  $crit_time         = '10',
){
  $template =  $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
  }
  @@nagios_service { "website_ssl_${website_name}_${path}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => "check_website_ssl!${warn_time}!${crit_time}!${website_name}!${path}!${port}!${expect_string}",
    service_description => "website_ssl_${website_name}",
    use                 => $template,
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}

