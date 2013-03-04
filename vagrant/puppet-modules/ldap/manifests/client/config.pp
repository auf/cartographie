# == Class: ldap::config
class ldap::client::config {
  file { $ldap::params::ldapconf:
    ensure  => present,
    mode    => '0644',
    content => template('ldap/ldap-client.conf.erb')
  }
}
