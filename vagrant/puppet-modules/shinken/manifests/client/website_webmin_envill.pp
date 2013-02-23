define shinken::client::webmin_envill (
  $fqdn              = $::fqdn,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All',
  $poller_tag        = 'envill',
  $path              = '/',
  $business_critical = true,
  $port              = 10000
){
  @@nagios_service { "webmin_${name}_${path}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => "check_website!5!10!${name}!${path}!${port}",
    service_description => "webmin_${name}",
    use        => $business_critical ? { 
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}

