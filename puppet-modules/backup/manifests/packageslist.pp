class backup::packageslist {
  require backup::common
  # simple class to produce daily backups of a list of the installed DEB packages
  # every day, kept for a week.
  file { "/etc/cron.daily/backuppackageslist":
    ensure => "file",
    source => "puppet:///modules/backup/backuppackageslist",
    owner => root,
    mode => 755;
  }
}
