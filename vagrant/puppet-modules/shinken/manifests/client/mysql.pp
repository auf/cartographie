class shinken::client::mysql (
  $fqdn              = $::fqdn,
  $hostname          = $::hostname,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All,LocalChecks',
  $poller_tag        = 'Main',
  $business_critical = true
){
  @@nagios_service { "mysql_${fqdn}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => 'check_nrpe!check_mysql',
    service_description => 'Mysql',
    use                 => $business_critical ? { 
        true        => 'Template_Service_Critical',
        false       => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
}
