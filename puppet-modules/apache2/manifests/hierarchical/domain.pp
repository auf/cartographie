define apache2::hierarchical::domain (
  hierarchical_folder_path,
) {

  include apache2::variables

  file { "${apache2::variables::apache_root_path}/sites-available/${hierarchical_folder_path}":
    ensure  => directory,
    mode    => '0755',
  }

  file { "${apache2::variables::apache_log_path}/${hierarchical_folder_path}":
    ensure  => directory,
    mode    => '0755',
  }

  file { "${apache2::variables::apache_doc_path}/${hierarchical_folder_path}":
    ensure  => directory,
    mode    => '0755',
  }

  $logrotate_path = regsubst( "${apache2::variables::apache_log_path}/${hierarchical_folder_path}", '//', '/')
  file { "${apache2::variables::logrotate_conf_path}/apache2-${site_domain}":
    ensure  => file,
    mode    => '0644',
    content => template('apache2/logrotate-apache2.erb')
  }
}

