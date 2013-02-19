class backup::rsnapshot::server (
  $rsnapshot_conf_dir        = '/etc/rsnapshot.d',
) {
  package { "rsync": ensure => present }
  package { "rsnapshot": ensure => present }
  File <<| tag == "rsnapshot-client-$fqdn" |>>
  Cron <<| tag == "rsnapshot-client-$fqdn" |>>
}
