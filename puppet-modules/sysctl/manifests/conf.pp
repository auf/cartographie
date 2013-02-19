define sysctl::conf ( $value ) {
  include sysctl
  # guid of this entry
  $key = $name

  $context = "/files/etc/sysctl.conf"

  augeas { "sysctl_conf/$key":
    context => "$context",
    onlyif  => "get $key != '$value'",
    changes => "set $key '$value'",
    notify  => Class["sysctl::reload"],
  }
}
