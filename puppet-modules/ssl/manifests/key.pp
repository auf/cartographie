define ssl::key (
  source = "puppet:///files/ssl/key_${name}.key",
  ) {
  include ssl::variables
  include ssl::common

  file { "${ssl::variables::ssl_private}/key_${name}.key":
    ensure  => file,
    mode    => '0440',
    group   => 'ssl-cert',
    source  => $source,
    require => Package['openssl']
  }
}
