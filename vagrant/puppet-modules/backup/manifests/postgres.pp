class backup::postgres {
  require backup::common
  # simple class to produce daily backups of a list of the installed DEB packages
  # every day, kept for a week.
  file { "/etc/cron.daily/backuppostgres":
    ensure => "file",
    source => "puppet:///modules/backup/backuppostgres",
    owner => root,
    mode => 755;
  }
}
