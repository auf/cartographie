define ssl::cert (
  $source = "puppet:///files/ssl/cert_${name}.crt",
) {
  include ssl::variables
  include ssl::common

  file { "${ssl::variables::ssl_local_certs}/cert_${name}.crt" :
    ensure  => file,
    mode    => '0444',
    group   => 'ssl-cert',
    source  => $source,
    require => Package['openssl'],
    notify  => Exec['update-ca-certificates'],
  }
}
