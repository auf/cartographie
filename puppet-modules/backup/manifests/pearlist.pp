class backup::pearlist {
  require backup::common
  # simple class to produce daily backups of a list of the installed DEB packages
  # every day, kept for a week.
  file { "/etc/cron.daily/backuppearlist":
    ensure => "file",
    source => "puppet:///modules/backup/backuppearlist",
    owner => root,
    mode => 755;
  }
}
