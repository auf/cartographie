define shinken::module (
  $module_type = false,
  $customcontent = false
) {
  include shinken::variables
  if ! $module_type { fail("You must set a module_type") }

  concat::fragment { $name:
    target  => $shinken::variables::configfile,
    order   => 30,
    content => template('shinken/module.erb'),
  }
}

