define apache2::namevirtualhost (
  $ports     = ['80'],
  $protocol  = 'http',
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

  concat::fragment { "NameVirtualhost_${name}":
    target  => '/etc/apache2/ports.conf',
    content => template('apache2/namevirtualhost.erb'),
    order   => 20,
  }
}

define apache2::namevirtualhost::ssl (
  $ports     = ['443'],
  $protocol  = 'https',
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

  concat::fragment { "NameVirtualhostssl${name}":
    target  => '/etc/apache2/ports.conf',
    content => template('apache2/namevirtualhost.erb'),
    order   => 20,
  }
}
