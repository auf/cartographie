class puppet::client (
  $service         = 'managed',
  $ensure          = running,
  $enable          = true,
  $runinterval     = '1800',
  $environment     = 'production',
  $certname        = '',
  $server          = 'puppet',
  $masterport      = '8140',
  $report          = true,
  $kick            = false,
  $kick_from       = "puppet.${::domain}",
  $splay           = true,
  $cron            = false,
  $logfacility     = 'daemon',
  $configtimeout   = '120',
  $certname        = undef,
  $lightclient     = false,
  $etckeeperactive = false,
) {

  include puppet::variables
  include puppet::config::common

  if empty( $certname ) {
    if $ec2_instance_id {
      $my_certname = $ec2_instance_id
    }
    elsif $::fqdn {
      $my_certname = downcase($::fqdn)
    }
    elsif $::hostname {
      $my_certname = downcase($::hostname)
    }
  }
  else {
    $my_certname = $certname
  }

  if $my_certname == '' {
    fail( 'Unable to determine a proper value for certname. This will cause Puppet to fail on next run, so we stop here.')
  }

  $autosplay = ( $runinterval * 95 ) / 100
  $splaylimit = $splay ? {
    true     => $autosplay,
    false    => 0,
    default  => $splay
  }

  if $runinterval < $splaylimit {
    fail('splay cannot be higher than runinterval')
  }

  if $cron == true and $ensure == 'running' {
    fail('cron and ensure are true! choose one way to run the puppet agent')
  }

  anchor { 'puppet::begin': }
  anchor { 'puppet::end': }

  Anchor[ 'puppet::begin' ] -> class { 'puppet::client::install': lightclient => $lightclient } -> Class['puppet::client::config'] -> Anchor[ 'puppet::end' ]

  if $service != 'unmanaged' {
    Class['puppet::client::config'] -> Class['puppet::client::service'] -> Anchor[ 'puppet::end' ]
    class { 'puppet::client::service':
      ensure => $puppet::client::ensure,
      enable => $puppet::client::enable,
    }
  }

  if $cron {
    class { 'puppet::client::cron':
      runinterval => $puppet::client::runinterval,
      splaylimit  => $splaylimit,
    }
  }

  class { 'puppet::client::config':
    enable          => $puppet::client::enable,
    runinterval     => $puppet::client::runinterval,
    environment     => $puppet::client::environment,
    certname        => $puppet::client::my_certname,
    server          => $puppet::client::server,
    masterport      => $puppet::client::masterport,
    report          => $puppet::client::report,
    kick            => $puppet::client::kick,
    kick_from       => $puppet::client::kick_from,
    splay           => $puppet::client::splay,
    splaylimit      => $puppet::client::splaylimit,
    logfacility     => $puppet::client::logfacility,
    configtimeout   => $puppet::client::configtimeout,
    etckeeperactive => $puppet::client::etckeeperactive,
  }
}
