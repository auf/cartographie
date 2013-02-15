class puppet::master (
  $dnsaltnames                        = ['puppet', $::fqdn, "puppet.${domain}"],
  $puppetmaster_external_node         = false,
  $puppetmaster_external_node_script  = false,
  $puppet_db_server                   = $::fqdn,
  $puppet_db_port                     = '8081',
  $use_passenger                      = true,
  $reports                            = false,
  $reporturl                          = "http://puppetdashboard.${domain}/reports/upload",
  $autosign                           = false,
) {

  Class['puppet::client'] -> Class['puppet::master']
  Class['puppet::master::install'] -> Class['puppet::master::config'] ~> Class['puppet::master::service']
  class { 'puppet::master::install': }
  class { 'puppet::master::config':
    dnsaltnames                       => $puppet::master::dnsaltnames,
    puppetmaster_external_node        => $puppet::master::puppetmaster_external_node,
    puppetmaster_external_node_script => $puppet::master::puppetmaster_external_node_script,
    puppet_db_server                  => $puppet::master::puppet_db_server,
    puppet_db_port                    => $puppet::master::puppet_db_port,
    reports                           => $puppet::master::reports,
    reporturl                         => $puppet::master::reporturl,
    autosign                          => $puppet::master::autosign,
  }
  class { 'puppet::master::maintenance': }

  if $use_passenger {
    Class['puppet::master::config'] ~> Class['apache2::service']
    class { 'puppet::master::service':
      ensure => stopped,
      enable => false
    }
    include puppet::master::passenger::install
  }
  else {
    class { 'puppet::master::service': }
  }
}
