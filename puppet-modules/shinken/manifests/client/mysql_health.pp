class shinken::client::mysql_health (
  $fqdn              = $::fqdn,
  $hostname          = $::hostname,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All,LocalChecks',
  $poller_tag        = 'Main',
  $business_critical = true,
  $warning           = false,
  $critical          = false,
  $username          = '',
  $password          = ''
){
  @@nagios_service { "mysqlhealth_slaveio_${fqdn}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => "check_nrpe!check_mysql_slaveio!$username!$password",
    service_description => 'Mysq health - Slave IO - Running',
    use                 => $business_critical ? {
        true        => 'Template_Service_Critical',
        false       => 'Template_Service_Not_Critical',
        },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }                                                     
  @@nagios_service { "mysqlhealth_slavesql_${fqdn}":
    host_name           => $fqdn,
    check_interval      => undef,
    check_command       => "check_nrpe!check_mysql_slavesql!$username!$password",
    service_description => 'Mysq health - Slave SQL - Running',
    use                 => $business_critical ? {
        true        => 'Template_Service_Critical',
        false       => 'Template_Service_Not_Critical',
        },
    tag                 => $environment,
    servicegroups       => $extraservicegroup,
    poller_tag          => $poller_tag,
  }                                                     
}

### MySQL ###
#  nagios_command { 'check_mysql_connectiontime':
 #   command_line   => '$USER1$/check_mysql_health -H $HOSTADDRESS$ --warning $ARG1$ --critical $ARG2$ --username $ARG3$ --password $ARG4$ --mode connection-time'
 # }

#  nagios_command { 'check_mysql_slaveio':
#    command_line   => '$USER1$/check_mysql_health -H $HOSTADDRESS$ --username $ARG1$ --password $ARG2$ --mode slave-io-running'
#  }

#  nagios_command { 'check_mysql_slavesql':
#    command_line   => '$USER1$/check_mysql_health -H $HOSTADDRESS$ --username $ARG1$ --password $ARG2$ --mode slave-sql-running'
#  }

 # nagios_command { 'check_tcp_3306':
 #   command_line   => '$USER1$/check_tcp -H $HOSTADDRESS$ -p 3306'
 # }

#  package { [
#    'libdbd-mysql-perl', # vdegrandpre - Déclaration en double pour www1.tabtimes.com
#    'libdbi-perl' # vdegrandpre - Déclaration en double pour www1.tabtimes.com
#  ]:
#    ensure => present,
#  }
#}
