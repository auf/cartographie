define backup::rsnapshot::clientextra (
  $rsnapshot_conf_dir        = '/etc/rsnapshot.d',
  $client                    = undef,
  $server                    = undef,
  $backup_monitoring         = false,
  $backup_server             = 'sfl-backupvm-01.iweb-hcl.sfl',
  $rsnapshot_config_version  = '1.2',
  $rsnapshot_hourly_retain   = undef,
  $rsnapshot_daily_retain    = undef,
  $rsnapshot_weekly_retain   = undef,
  $rsnapshot_monthly_retain  = undef,
  $rsnapshot_ssh_args        = undef,
  $rsnapshot_rsync_long_args = undef,
  $rsnapshot_verbose         = '2',
  $rsnapshot_loglevel        = '3',
  $rsnapshot_logfile         = "/var/log/rsnapshot-${client}-${server}.log",
  $rsnapshot_lockfile        = "/var/run/rsnapshot-${client}-${server}.lock",
  $rsnapshot_exclude_dirs    = [ '/dev/', '/proc/', '/sys/', ],
  $rsnapshot_dirs2backup     = [ '/etc/', '/var/', ],
  $rsnapshot_host            = undef,
  $hourly_cron_hour          = undef,
  $hourly_cron_minute        = undef,
  $hourly_cron_month         = '*',
  $hourly_cron_monthday      = '*',
  $hourly_cron_weekday       = '*',
  $daily_cron_hour           = undef,
  $daily_cron_minute         = undef,
  $daily_cron_month          = '*',
  $daily_cron_monthday       = '*',
  $daily_cron_weekday        = '*',
  $weekly_cron_hour          = undef,
  $weekly_cron_minute        = undef,
  $weekly_cron_month         = '*',
  $weekly_cron_monthday      = '*',
  $weekly_cron_weekday       = undef,
  $monthly_cron_hour         = undef,
  $monthly_cron_minute       = undef,
  $monthly_cron_month        = '*',
  $monthly_cron_monthday     = undef,
  $monthly_cron_weekday      = '*',
) {
  if $rsnapshot_hourly_retain {
    cron { "cron_backup_${server}_${client}_hourly}":
      command  => "/usr/local/sysadmin/rsnapshot -v -c $rsnapshot_conf_dir/$client/$server hourly >> /var/backups/log/$client/$server.log",
      user     => root,
      hour     => $hourly_cron_hour,
      minute   => $hourly_cron_minute,
      month    => $hourly_cron_month,
      monthday => $hourly_cron_monthday,
      weekday  => $hourly_cron_weekday,
      tag      => "rsnapshot-client-$backup_server",
    }
  }
  if $rsnapshot_daily_retain {
    cron { "cron_backup_${server}_${client}_daily":
      command  => "/usr/local/sysadmin/rsnapshot -v -c $rsnapshot_conf_dir/$client/$server daily >> /var/backups/log/$client/$server.log",
      user     => root,
      hour     => $daily_cron_hour,
      minute   => $daily_cron_minute,
      month    => $daily_cron_month,
      monthday => $daily_cron_monthday,
      weekday  => $daily_cron_weekday,
      tag      => "rsnapshot-client-$backup_server",
    }
  }
  if $rsnapshot_weekly_retain {
    cron { "cron_backup_${server}_${client}_weekly":
      command  => "/usr/local/sysadmin/rsnapshot -v -c $rsnapshot_conf_dir/$client/$server weekly >> /var/backups/log/$client/$server.log",
      user     => root,
      hour     => $weekly_cron_hour,
      minute   => $weekly_cron_minute,
      month    => $weekly_cron_month,
      monthday => $weekly_cron_monthday,
      weekday  => $weekly_cron_weekday,
      tag      => "rsnapshot-client-$backup_server",
    }
  }
  if $rsnapshot_monthly_retain {
    cron { "cron_backup_${server}_${client}_monthly":
      command  => "/usr/local/sysadmin/rsnapshot -v -c $rsnapshot_conf_dir/$client/$server monthly >> /var/backups/log/$client/$server.log",
      user     => root,
      hour     => $monthly_cron_hour,
      minute   => $monthly_cron_minute,
      month    => $monthly_cron_month,
      monthday => $monthly_cron_monthday,
      weekday  => $monthly_cron_weekday,
      tag      => "rsnapshot-client-$backup_server",
    }
  }

  exec { "dir_${client}_${server}_datadir_confdir":
    command => "mkdir -m=u+rwx -p /var/backups/rsnapshot/$client/$server ${rsnapshot_conf_dir}/${client} /var/backups/log/$client/$server",
    path    => ["/bin", "/usr/bin", "/usr/sbin"], 
    tag     => "rsnapshot-client-$backup_server",
  }

  file { "${rsnapshot_conf_dir}/${client}/${server}":
    ensure  => file,
    mode    => 0644,
    content => template('backup/rsnapshot.conf.erb'),
    tag     => "rsnapshot-client-$backup_server",
  }
  if $backup_monitoring == true {
    nagios_service { "RSnapshot_status_${hostname}":
      check_command          => "check_dummy!2!No_report_received",
      check_freshness        => 1,
      freshness_threshold    => 108000,
      passive_checks_enabled => 1,
      active_checks_enabled  => 0,
      flap_detection_enabled => 0,
      service_description    => 'Rsnapshot status',
      notification_period    => "WorkHours",
      max_check_attempts     => 1,
      tag                    => "${environment}"
    }
  }

}
