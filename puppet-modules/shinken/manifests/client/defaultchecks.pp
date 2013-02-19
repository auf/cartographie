class shinken::client::defaultchecks (
  $ipaddress          = $::ipaddress,
  $fqdn               = $::fqdn,
  $hostname           = $::hostname,
  $extrahostgroup     = '+All',
  $extraservicegroup  = '+All,DefaultChecks',
  $realm              = 'Main',
  $business_critical  = true,
  $use_ip             = false,
  $poller_tag         = 'Main',
  $parents            = undef,
  $check_interval     = undef,
  $retry_interval     = undef,
  $max_check_attempts = undef,
  $can_ping           = true,
  $can_use_nrpe       = true,
  $can_do_ntp         = true,
  $trace_cpu          = true,
  $notes              = 'NoClient',
){
  if $can_ping { 
    @@nagios_host { $fqdn:
     address    => $use_ip ? {
       true  => $ipaddress,
       false => $fqdn,
     },
     tag        => $environment,
     use        => $business_critical ? {
       true  => 'Template_Host_Critical',
       false => 'Template_Host_Not_Critical',
     },
     parents    => $parents,
     hostgroups => $extrahostgroup,
     realm      => $realm,
     poller_tag => $poller_tag,
     notes      => $notes,
    }
  } else {
    @@nagios_host { $fqdn:
     address    => $use_ip ? {
       true  => $ipaddress,
       false => $fqdn,
     },
     tag        => $environment,
     use        => $business_critical ? {
       true  => 'Template_Host_Critical',
       false => 'Template_Host_Not_Critical',
     },
     check_command => $can_use_nrpe ? {
        true  => "check_tcp!$fqdn!5666",
        false => '',
     },
     parents    => $parents,
     hostgroups => $extrahostgroup,
     realm      => $realm,
     poller_tag => $poller_tag,
     notes      => $notes,
    }
  }

  # this service is not considered critical by default.
  @@nagios_service { "Puppet_${fqdn}":
    host_name           => $fqdn,
    check_interval      => $check_interval,
    retry_interval      => $retry_interval,
    max_check_attempts  => $max_check_attempts,
    check_command       => 'check_nrpe!check_puppet_agent',
    service_description => 'Puppet agent is running',
    use                 => 'Template_Service_Not_Critical',
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }

  if $can_ping {
  @@nagios_service { "Ping_${fqdn}":
    host_name           => $fqdn,
    check_interval      => $check_interval,
    retry_interval      => $retry_interval,
    max_check_attempts  => $max_check_attempts,
    check_command       => 'check_ping',
    service_description => 'Ping',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }
  }

  if $can_use_nrpe {
    class { 'shinken::client::disks':
      fqdn              => $fqdn,
      hostname          => $hostname,
      extrahostgroup    => $extrahostgroup,
      extraservicegroup => $extraservicegroup,
      business_critical => $business_critical,
      poller_tag        => $poller_tag,
    }
  @@nagios_service { "Cron_${fqdn}":
    host_name           => $fqdn,
    check_command       => $::operatingsystem ? {
    'CentOS' => 'check_nrpe!check_crond', 
    'Fedora' => 'check_nrpe!check_crond',
    'RedHatEnterpriseServer' => 'check_nrpe!check_crond',
    'RedHat' => 'check_nrpe!check_crond',
    'Scientific' => 'check_nrpe!check_crond',
    default => 'check_nrpe!check_cron',
    },
    service_description => 'Cron is running',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag => $poller_tag,
  }

  # this service is not considered critical by default.
  if $can_do_ntp {
  @@nagios_service { "ntptime_${fqdn}":
    host_name           => $fqdn,
    check_interval      => $check_interval,
    retry_interval      => $retry_interval,
    max_check_attempts  => $max_check_attempts,
    check_command       => 'check_nrpe!check_ntp_time',
    service_description => 'Time is correct with NTP',
    use                 => 'Template_Service_Not_Critical',
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag => $poller_tag,
  }
  }
  @@nagios_service { "memory_${fqdn}":
    host_name           => $fqdn,
    check_interval      => $check_interval,
    retry_interval      => $retry_interval,
    max_check_attempts  => $max_check_attempts,
    check_command       => 'check_nrpe!check_memory',
    service_description => 'Available memory',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag => $poller_tag,
  }

  @@nagios_service { "Load_${fqdn}":
    host_name           => $fqdn,
    check_command       => 'check_nrpe!check_load',
    service_description => 'Load',
    use        => $business_critical ? {
      true  => 'Template_Service_Critical',
      false => 'Template_Service_Not_Critical',
    },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag => $poller_tag,
  }
  if $trace_cpu {
    include shinken::client::cpu::requirements
    class { 'shinken::client::cpu':
      fqdn              => $fqdn,
      hostname          => $hostname,
      extrahostgroup    => $extrahostgroup,
      extraservicegroup => $extraservicegroup,
      business_critical => $business_critical,
      poller_tag        => $poller_tag,
      }
    }
  }
}
