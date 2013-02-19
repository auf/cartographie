define shinken::poller (
  $address = $::ipaddress,
  $port    = 7771,
  $spare   = 0,
  $realm   = false,
  $manage_sub_realms = 0,
  $poller_tags = false,
  $modules     = false,
  $min_workers = 4,
  $max_workers = 4
) {
  include shinken::variables
  
  concat::fragment { $name:
    target  => $shinken::variables::configfile,
    order   => 30,
    content => template('shinken/poller.erb'),
  }
}
