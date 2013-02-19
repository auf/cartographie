# == Class: shinken::client::ldap
#
# This class test access to an ldap server
#
# === Parameters
# [*tls*]
#   List of tls setup to check:
#  'starttls', 'ssl', or 'none'
class shinken::client::ldap (
  $fqdn              = $::fqdn,
  $extrahostgroup    = '+All',
  $extraservicegroup = '+All',
  $poller_tag        = 'Main',
  $business_critical = true,
  $base              = 'dc=example,dc=com',
  $tls               = ['none'],
  $ldap_server       = $::fqdn,
){

  $use = $business_critical ? {
    true  => 'Template_Service_Critical',
    false => 'Template_Service_Not_Critical',
  }

  if 'starttls' in $tls {
    shinken::client::ldap::check { "ldap_tls_${fqdn}_${base}":
      check_command => "check_ldap_tls!4!8!${base}!${ldap_server}",
      description   => 'LDAP with StartTLS'
    }
  }
  if 'ssl' in $tls {
    shinken::client::ldap::check { "ldaps_${fqdn}_${base}":
      check_command => "check_ldaps!4!8!${base}!${ldap_server}",
      description   => 'LDAP over SSL - ldaps'
    }
  }
  if 'none' in $tls {
    shinken::client::ldap::check { "ldap_${fqdn}_${base}":
      check_command => "check_ldap!4!8!${base}",
      description   => 'LDAP - unencrypted'
    }
  }
}

