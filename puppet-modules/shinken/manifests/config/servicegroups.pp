class shinken::config::servicegroups {
  nagios_servicegroup { 'All': ensure => present }
  nagios_servicegroup { 'Linux': }
  nagios_servicegroup { 'Database': }
  nagios_servicegroup { 'Web': }
  nagios_servicegroup { 'Backup': }
}
