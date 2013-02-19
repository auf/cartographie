define shinken::realm (
  $realm_members = false,
  $isdefault     = 0
) {
  include shinken::variables
  
  concat::fragment { $name:
    target  => $shinken::variables::configfile,
    order   => 60,
    content => template('shinken/realm.erb'),
  }
}

