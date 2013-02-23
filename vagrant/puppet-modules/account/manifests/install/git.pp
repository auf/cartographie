class account::install::git {
  $package_name = $osfamily ? {
    'RedHat' => 'git',
    'Debian' => 'git-core',
    default  => 'git'
  }
  package { $package_name:
    ensure => 'present',
  }
  package { 'tig':
    ensure  => 'present',
    require => Package[$package_name],
  }
}
