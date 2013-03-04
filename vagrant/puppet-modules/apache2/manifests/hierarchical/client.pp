define apache2::hierarchical::client (
  $client,
) {

  include apache2::variables

  file { "${apache2::variables::apache_root_path}/sites-available/${client}":
    ensure  => directory,
    mode    => '0755',
  }

  file { "${apache2::variables::apache_log_path}/${client}":
    ensure  => directory,
    mode    => '0755',
  }

  file { "${apache2::variables::apache_doc_path}/${client}":
    ensure  => directory,
    mode    => '0755',
  }
}
