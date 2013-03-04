class account::install::vim {
  package { 'vim':
    ensure => 'present',
  }
  package { 'vim-scripts':
    ensure  => 'present',
    require => Package['vim'],
  }
  package { 'vim-addon-manager':
    ensure  => 'present',
    require => Package['vim-scripts'],
  }
}
