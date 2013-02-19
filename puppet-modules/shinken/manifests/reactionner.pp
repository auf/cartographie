define shinken::reactionner (
  $modules,
  $address = $::ipaddress,
  $port    = 7769,
  $spare   = 0,
  $realm   = false,
  $manage_sub_realms = 1,
  $reactionner_tags = false
) {
  include shinken::variables
  
  concat::fragment { $name:
    target  => $shinken::variables::configfile,
    order   => 40,
    content => template('shinken/reactionner.erb'),
  }
}
