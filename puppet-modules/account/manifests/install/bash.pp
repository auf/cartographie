class account::install::bash {
  package { 'bash':
    ensure => 'present',
  }
  package { 'bash-completion':
    ensure  => 'present',
    require => Package['bash'],
  }
}
