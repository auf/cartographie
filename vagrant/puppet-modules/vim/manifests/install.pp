class vim::install (
  $puppet = false
  ) {
  include vim::params
  package { $vim::params::pkgs:
    ensure => present,
  }
  if $puppet and $osfamily == 'Debian' { 
    package { 'vim-puppet':
      ensure => present,
    }
  }
}
