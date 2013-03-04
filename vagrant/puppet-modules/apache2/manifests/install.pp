# do not use directly
class apache2::install (
  ) {

  include apache2::variables

  # Make the variables available for websites
  $my_apache2_listen_ips     = $apache2_listen_ips
  $my_apache2_listen_ips_ssl = $apache2_listen_ips_ssl

  package { $apache2::variables::apache_package_name:
    ensure => present
  }

  user { $apache2::variables::apache_user:
    ensure  => present,
  }

  group { $apache2::variables::apache_group:
    ensure  => present,
  }
}

