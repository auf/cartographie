class puppet::db (
  $java_args = "-Xmx512m ",
  $host      = 'localhost',
  $ssl_host  = $::fqdn,
) {

  Class[ "${module_name}::db::install" ] ->
    Class[ "${module_name}::db::config" ] ~>
      Class[ "${module_name}::db::service" ]

  class { 'puppet::db::install': }
  class { 'puppet::db::config':
    java_args => $puppet::db::java_args,
    host      => $puppet::db::host,
    ssl_host  => $puppet::db::ssl_host,
  }
  class { 'puppet::db::service': }
}
