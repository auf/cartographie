class shinken::client::shinken (
  $fqdn              = $::fqdn,
  $hostname          = $::hostname,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All',
  $business_critical = true,
  $poller_tag        = 'Main'
){
  @@nagios_service { "shinken_arbiter_${fqdn}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => 'check_shinken_arbiter',
    service_description => 'Shinken Arbiter status',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
  @@nagios_service { "shinken_poller_${fqdn}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => 'check_shinken_poller',
    service_description => 'Shinken Poller status',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }

  @@nagios_service { "shinken_broker_${fqdn}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => 'check_shinken_broker',
    service_description => 'Shinken Broker status',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }

  @@nagios_service { "shinken_scheduler_${fqdn}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => 'check_shinken_scheduler',
    service_description => 'Shinken Scheduler status',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }

  @@nagios_service { "shinken_reactionner_${fqdn}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => 'check_shinken_reactionner',
    service_description => 'Shinken Reactionner status',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }


}

