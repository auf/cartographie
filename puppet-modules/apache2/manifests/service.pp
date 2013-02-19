class apache2::service {
  include apache2::variables

  service { $apache2::variables::apache_service_name:
    ensure      => running,
    enable      => true,
    hasstatus   => true,
    hasrestart  => true,
  }

  # Notify this when apache needs a reload. This is only needed when sites are added or removed
  # since a full restart then would be a waste of time.
  exec { 'reload-apache2':
    command      => "/etc/init.d/${apache2::variables::apache_service_name} reload",
    refreshonly  => true,
  }

  #When the module-config changes, a force-reload is needed.
  exec { 'force-reload-apache2':
    command      => '/etc/init.d/apache2 force-reload',
    refreshonly  => true,
  }
}

