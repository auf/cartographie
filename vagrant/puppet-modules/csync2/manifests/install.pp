class csync2::install ($inet=true) {
	package {'csync2':
    ensure => present
  }
  if $inet == true {
    package { 'openbsd-inetd':
      ensure => present
    }
  }
}
