class puppet::client::cron (
  $runinterval,
  $splaylimit,
) {

  $minutes = $runinterval / 60
  cron { 'puppet':
    command => "puppet agent --onetime --pidfile /var/run/puppet/onetime.pid",
    user    => 'root',
    minute  => "*/${minutes}",
  }
}
