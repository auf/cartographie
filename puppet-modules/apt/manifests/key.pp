# = Define: key
#
# === Parameters:
#
# $keyid:: The repository keyid to be added to apt trusted keys
# $ensure::  Whether we want to add or remove this key
# $gpg_key_server (pgp.mit.edu):: The server from which to get the key
define apt::key(
  $keyid,
  $ensure         = present,
  $gpg_key_server = 'keys.gnupg.net'
  ) {
  case $ensure {
    present: {
      exec { "Import ${name} ${keyid} to apt keystore":
        path        => "/bin:/usr/bin",
        command     => "gpg --keyserver ${gpg_key_server} --keyserver-options timeout=10 --recv-keys $keyid && gpg --export --armor $keyid | apt-key add -",
        user        => "root",
        group       => "root",
        unless      => "apt-key list | grep $keyid",
        logoutput   => on_failure,
      }
    }
    absent:  {
      exec { "Remove $keyid from apt keystore":
        path    => "/bin:/usr/bin",
        command => "apt-key del $keyid",
        user    => "root",
        group   => "root",
        onlyif  => "apt-key list | grep $keyid",
      }
    }
    default: {
      fail "Invalid 'ensure' value '$ensure' for apt::key"
    }
  }
}