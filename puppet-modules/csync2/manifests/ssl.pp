class csync2::ssl (
  $sslcert = 'puppet:///files/csync2/csync2_ssl_cert.pem',
  $sslkey = 'puppet:///files/csync2/csync2_ssl_key.pem'
  ) {
  file { '/etc/csync2_ssl_cert.pem' :
    source  => $sslcert,
    ensure  => file,
    mode    => 600,
    require => Class['csync2::install'],
  }
  file { '/etc/csync2_ssl_key.pem' :
    source  => $sslkey,
    ensure  => file,
    mode    => 600,
    require => Class['csync2::install'],
  } 
}
