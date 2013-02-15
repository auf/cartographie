class puppet::db::install {

  user { 'puppetdb':
    ensure      => present,
    home        => '/usr/share/puppetdb',
    managehome  => true,
    shell       => '/bin/false',
    allowdupe   => false,
    uid         => '430',
    gid         => 'puppetdb',
  }

  group { 'puppetdb':
    gid => '430',
  }

  package { 'puppetdb':
    ensure  => present,
    require => User[ 'puppetdb' ],
  }
}
