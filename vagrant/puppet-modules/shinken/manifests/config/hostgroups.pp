class shinken::config::hostgroups {
  nagios_hostgroup { 'All': ensure => present }
  nagios_hostgroup { 'Linux': }
  nagios_hostgroup { '24x7': }
  nagios_hostgroup { 'WorkHours': }
  nagios_hostgroup { 'Never': }
}
