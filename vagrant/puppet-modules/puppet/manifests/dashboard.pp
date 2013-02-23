class puppet::dashboard (
  $db_password,
  $db_host               = 'localhost',
  $db_port               = '3306',
  $db_name               = 'puppet_dashboard',
  $db_user               = 'puppet',
  $ca_server             = 'puppet',
  $ca_port               = '8140',
  $inventory_server      = 'puppet',
  $inventory_port        = '8140',
  $enable_inventory      = false,
  $read_only_mode        = true,
  $time_zone             = 'Paris',
  $expire_old_reports    = 'upto=1 unit=mon',
  $manage_mysql          = true,
  $reporting_cutoff      = '2000',
) {

  validate_string( $db_password, $db_name, $db_server, $db_user, $ca_server, $ca_port, $inventory_server, $inventory_port, $time_zone, $expire_old_reports )
  validate_bool( $enable_inventory, $read_only_mode)

  include apache2::variables

  Class['puppet::dashboard::install'] ->
    Class['puppet::dashboard::config'] ~>
      Class['puppet::dashboard::service', 'apache2::service' ] ->
        Class['puppet::dashboard::maintenance']

  class { 'puppet::dashboard::install': }
  class { 'puppet::dashboard::config':
    db_host               => $puppet::dashboard::db_host,
    db_port               => $puppet::dashboard::db_port,
    db_name               => $puppet::dashboard::db_name,
    db_user               => $puppet::dashboard::db_user,
    db_password           => $puppet::dashboard::db_password,
    ca_server             => $puppet::dashboard::ca_server,
    ca_port               => $puppet::dashboard::ca_port,
    inventory_server      => $puppet::dashboard::inventory_server,
    inventory_port        => $puppet::dashboard::inventory_port,
    enable_inventory      => $puppet::dashboard::enable_inventory,
    read_only_mode => $puppet::dashboard::read_only_mode,
    time_zone    => $puppet::dashboard::time_zone,
    manage_mysql          => $puppet::dashboard::manage_mysql,
    reporting_cutoff      => $puppet::dashboard::reporting_cutoff,
  }
  class { 'puppet::dashboard::service': }
  class { 'puppet::dashboard::maintenance':
    expire_old_reports => $puppet::dashboard::expire_old_reports
  }
}
