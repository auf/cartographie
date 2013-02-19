class vsftpd (
  $vsftpd_anonymous_enable = "NO",
  $vsftpd_extralines = ""
) {
  package {'vsftpd': ensure => present}
  service {'vsftpd':
    ensure => running,
    require => Package['vsftpd'],
  }
  file {'/etc/vsftpd.conf': 
    content => template("vsftpd/vsftpd.conf.erb"),
    require => Package['vsftpd'],
    notify => Service['vsftpd'],
  }
}
