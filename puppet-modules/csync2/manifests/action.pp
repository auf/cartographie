define csync2::action (
  pattern,
  cmd,
  logfile = [],
  dolocal = false
) {
  if ! $pattern { fail("pattern not defined!") }
  if ! $cmd { fail("cmd not defined!") }

  concat::fragment { "csync2_${name}":
    target  => '/etc/csync2.cfg',
    order   => 60,
    content => template("csync2/action.erb")
  }
}
  
