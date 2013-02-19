class shinken::config (
  $resources_source_folder,
  $resources_folder         = '/etc/nagios/resources',
  $monitored_environments   = [ 'development', 'production'],
  $extraconfigfile          = false,
  $extraconfigfilesourceurl = false,
) {

  if $extraconfigfile and $extraconfigfilesourceurl {
    file { "/etc/nagios/${extraconfigfile}":
      ensure  => present,
      owner   => 'shinken',
      group   => 'shinken',
      source  => $extraconfigfilesourceurl,
      require => Package['shinken'],
    }
  }

  #objects config will be put there by puppet
  file { '/etc/nagios':
    ensure          => directory,
    owner           => 'shinken',
    group           => 'shinken',
    recurse         => true,
    checksum        => mtime,
    require         => Package['shinken'],
  }
  file { '/etc/shinken':
    ensure          => directory,
    owner           => 'shinken',
    group           => 'shinken',
    recurse         => true,
    checksum        => mtime,
    require         => Package['shinken'],
  }

  #tell shinken to look into /etc/nagios for configs
  file { '/etc/shinken/nagios.cfg':
    ensure  => file,
    owner   => 'shinken',
    group   => 'shinken',
    content  => template('shinken/nagios.cfg.erb'),
    require => Package['shinken'],
  }
  
  file { '/etc/shinken/resource.cfg':
    ensure  => file,
    owner   => 'shinken',
    group   => 'shinken',
    source  => 'puppet:///modules/shinken/resource.cfg',
    require => Package['shinken'],
  }

  file { '/etc/shinken/templates.cfg':
    ensure  => file,
    owner   => 'shinken',
    group   => 'shinken',
    source  => 'puppet:///modules/shinken/templates.cfg',
    require => Package['shinken'],
  }
  
  file { $resources_folder:
    ensure  => directory,
    owner   => 'shinken',
    group   => 'shinken',
    recurse => true,
    source  => $resources_source_folder,
    require => Package['shinken'],
  }
}
