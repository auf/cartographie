class sysctl::reload {
   exec { "sysctl-load":
      command     => 'sysctl -p',
      alias       => "sysctl",
      refreshonly => true,
      subscribe   => File["sysctl_conf"],
   }
}
