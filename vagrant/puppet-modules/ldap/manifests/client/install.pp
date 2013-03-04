# don't call this class directly, use ldap::client
class ldap::client::install {
  package { $ldap::params::packages:
    ensure => present
  }
}
