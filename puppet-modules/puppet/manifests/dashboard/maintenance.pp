class puppet::dashboard::maintenance (
  $expire_old_reports
) {

  cron { 'dashboard_optimize_database':
    command     => '(cd /usr/share/puppet-dashboard/ && rake RAILS_ENV=production db:raw:optimize',
    environment => 'RAILS_ENV=production',
    minute      => 17,
    hour        => 5,
    monthday    => 3,
  }

  if $expire_old_reports {
    cron { 'dashboard_expire_old_reports':
      command     => "(cd /usr/share/puppet-dashboard/ && rake RAILS_ENV=production reports:prune ${expire_old_reports}) > /dev/null",
      environment => 'RAILS_ENV=production',
      minute      => 30,
      hour        => 5,
    }
  }
}
