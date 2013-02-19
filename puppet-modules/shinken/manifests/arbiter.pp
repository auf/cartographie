define shinken::arbiter (
  $address = $::ipaddress,
  $port    = 7770,
  $spare   = 0,
  $modules = false
) {
  include shinken::variables
  
  concat::fragment { $name:
    target  => $shinken::variables::configfile,
    order   => 10,
    content => template('shinken/arbiter.erb'),
  }
}
