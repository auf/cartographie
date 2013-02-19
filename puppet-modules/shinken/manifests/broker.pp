define shinken::broker (
  $modules = false,
  $address = $::ipaddress,
  $port    = 7772,
  $spare   = 0,
  $realm   = false,
  $manage_sub_realms = 1,
  $manage_arbiters = 1
) {
  include shinken::variables
  
  concat::fragment { $name:
    target  => $shinken::variables::configfile,
    order   => 50,
    content => template('shinken/broker.erb'),
    }
}
