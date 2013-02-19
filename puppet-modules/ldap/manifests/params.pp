# == Class: ldap::params
class ldap::params {
  case $::osfamily {
    'RedHat': {
      $ldapconf = '/etc/ldap/ldap.conf'
      $tls_cacert = '/etc/pki/tls/cert.pem'
      $packages = [
        'ca-certificates',
        'openldap-clients'
      ]
    }
    'Debian': {
      $ldapconf = '/etc/ldap/ldap.conf'
      $tls_cacert = '/etc/ssl/certs/ca-certificates.crt'
      $packages = [
        'ca-certificates',
        'ldap-utils',
      ]
    }
    default: {
      fail('Unsupported OS')
    }
  }
}
