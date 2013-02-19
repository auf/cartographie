class backup::wiki::priape {
  
  require backup::common
  
  file { "/etc/cron.daily/backupwikipriape":
    ensure => "file",
    source => "puppet:///modules/backup/backupwikipriape",
    owner => backupwikipriape,
    mode => 755;
  }
}
