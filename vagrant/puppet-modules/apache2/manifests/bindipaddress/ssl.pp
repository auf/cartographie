define apache2::bindipaddress::ssl (
  $ports     = ['443'],
  $protocol  = 'https'
) {
  if $protocol in [ 'http', 'https'] { }
  else {
    fail('The supported protocols are http and https')
  }

  if $name != '*' {
    if $name in $::ipaddresses or $name == '127.0.0.1' { }
    else {
      fail ("IP address ${name} does not belong to me")
    }
  }

  concat::fragment { "Listen_SSl_${name}":
    target  => '/etc/apache2/ports.conf',
    content => template('apache2/bindipaddress.erb'),
    order   => 10,
  }
}
