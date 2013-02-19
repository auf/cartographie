class sysctl {
  include sysctl::reload
  file { "sysctl_conf":
    name => $operatingsystem ? {
      default => "/etc/sysctl.conf",
    },
  }
}
