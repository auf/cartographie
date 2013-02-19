define shinken::client::website (
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
  $tmp_pat2 = regsubst($path, '\?', '_')
  $tmp_path = regsubst($tmp_pat2, '=', '_')
  $service_description = "website_${website_name}_${tmp_path}_${port}"
  @@nagios_service { "website_${website_name}_${path}_${port}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => "check_website!${warn_time}!${crit_time}!${website_name}!${path}!${port}",
    service_description => "${service_description}",
    use        => $business_critical ? { 
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}

