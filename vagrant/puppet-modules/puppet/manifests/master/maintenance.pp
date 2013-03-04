class puppet::master::maintenance (
) {
  cron { 'puppet_master_reports_cleanup':
    command     => "/usr/bin/find /var/lib/puppet/reports -type f -mtime +15 -delete && /usr/bin/find /var/lib/puppet/reports -mindepth 1 -empty -type d -delete",
    minute      => '15',
    hour        => '5',
  }
}
