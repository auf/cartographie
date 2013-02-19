define shinken::scheduler (
  $address = $::ipaddress,
  $port    = 7768,
  $spare   = 0,
  $realm   = false,
  $modules = false,
  $manage_sub_realms = 1
) {
  include shinken::variables
  
  concat::fragment { $name:
    target  => $shinken::variables::configfile,
    order   => 20,
    content => template('shinken/scheduler.erb'),
  }
}
