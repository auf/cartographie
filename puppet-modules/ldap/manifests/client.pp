# == Class: ldap::client
#
# This will install openldap clients and basic configuration in
# /etc/{open,}ldap/ldap.conf
#
# === Parameters
#
# All parameters are documented in ldap.conf(5).
# [*tls_reqcert*]
#   Must be never, allow, try, demand or hard (default: try)
# [*uri*]
#   Default URI for ldap clients
# [*base*]
#   Default base
#
# === Variables
#
# No external variables are required.
#
# === Examples
#
#  class { 'ldap::client':
#    tls_reqcert => 'demand'
#  }
#
# === Authors
#
# Simon Piette <simon.piette@savoirfairelinux.com>
#
# === Copyright
#
# Copyright 2012 Savoir-faire Linux
# GPL 3.0
#
class ldap::client (
    $uri = '',
    $base = '',
    $tls_reqcert = 'try',
) {
  $valid_tls_reqcert = [ 'never', 'allow', 'try', 'demand', 'hard' ]
  if ! ($tls_reqcert in $valid_tls_reqcert) {
    fail("\$tls_request must be in ${valid_tls_reqcert}")
  }
  Class['ldap::params'] ->
  Class['ldap::client::install'] ->
  Class['ldap::client::config']
  class {'ldap::params': }
  class {'ldap::client::install': }
  class {'ldap::client::config': }
}
