# = Define: module
#
# * Installs or remove a module for apache2
#
# == Parameters
#
# $ensure:: Whether a module should be enabled or not
# $required_package ([apache2]):: The package this module needs to be installable/usable. (_INFO_: You do not need to repeat apache2 if you need to set this variable )
# $config (false #*template*|*source*):: Whether a configuration should be created for this module. If set, the config file must exist in Puppet and be named like the module
define apache2::module (
  $ensure           = 'present',
  $required_package = apache2,
  $base_config      = false,
  $config           = false,
  $module_real_name = false
  ) {


  Class['apache2'] -> Apache2::Module[$name]

  # Reload apache if any module related operation is done
  Apache2::Module[$name] ~> Exec['reload-apache2']

  include apache2::variables

  if $jkoptions {} else {
    $jkoptions = [
      '+ForwardKeySize',
      '+ForwardURICompat',
      '+ForwardSSLCertChain',
      '-ForwardDirectories'
      ]
  }

  realize Package[$required_package]

  if $::osfamily == 'RedHat' {
    file { "${apache2::variables::apache_root_path}/mods-available/${name}.load":
      ensure  => file,
      content => template('apache2/module_load.erb'),
      require => Package[$required_package]
    }

    # Sometimes the module name does not match the file name.
    # Currently only seen mod_php5 -> libphp5 behave like this
    if $module_real_name {
      file { "${apache2::variables::apache_root_path}/modules/mod_${name}.so":
        ensure => symlink,
        target => "${apache2::variables::apache_root_path}/modules/${module_real_name}.so"
      }
    }

    file { "${apache2::variables::apache_root_path}/mods-enabled/${name}.load":
      ensure  => $ensure,
      target  => "${apache2::variables::apache_root_path}/mods-available/${name}.load",
      require => Package[$required_package],
    }

    #This intend to just copy package provided config so that it is not in httpd.conf
    if $base_config {
      file { "${apache2::variables::apache_root_path}/mods-available/${name}.conf":
        ensure  => file,
        source  => "puppet:///modules/apache2/base_config/${name}.conf",
        require => Package[$required_package],
      }

      file { "${apache2::variables::apache_root_path}/mods-enabled/${name}.conf":
        ensure  => $ensure,
        target  => "${apache2::variables::apache_root_path}/mods-available/${name}.conf",
        require => Package[$required_package],
      }
    }

  } else {
    #Use standard tools under Debian like OS
    case $ensure {
      'present' : {
        exec { "/usr/sbin/a2enmod ${name}":
          unless  => "test -L ${apache2::variables::apache_root_path}/mods-enabled/${name}.load",
          require => Package[$required_package],
        }
      }
      'absent': {
        exec { "/usr/sbin/a2dismod ${name}":
          onlyif => "test -L ${apache2::variables::apache_root_path}/mods-enabled/${name}.load",
        }
      }
      default: { err ( "Unknown ensure value: ${ensure}" ) }
    }
  }

  case $config {
    'template': {
      file { "${apache2::variables::apache_root_path}/conf.d/${title}.conf":
        ensure  => file,
        mode    => '0644',
        content => template("apache2/${title}.conf.erb"),
      }
    }
    'source': {
      file { "${apache2::variables::apache_root_path}/conf.d/${title}.conf":
        ensure => file,
        mode   => '0644',
        source => "puppet:///modules/apache2/${title}.conf",
      }
    }
    default: { }
  }
}
