class backup::wiki::sfl {
  
  require backup::common
  
  file { "/etc/cron.daily/backupwikisfl":
    ensure => "file",
    source => "puppet:///modules/backup/backupwikisfl",
    owner => www-data,
    mode => 755;
  }

#  file { "/sysadmin/ssh/backupwikisfl":
#    ensure => "file",
#    source => "puppet://modules/backup/backupwikisfl.ssh",
#    owner => backupwikisfl,
#    mode => 600;
#  }
}
