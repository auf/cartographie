# = Define: ppa
#
# === Parameters:
#
# $repo:: The repository name at launchpad
define apt::ppa(
  $repo,
  $key  = false
  ) {
  $reponame = regsubst($repo,"/","-")
  exec { "add-apt-repository_${repo}":
      command => "add-apt-repository ppa:${repo}",
      unless  => "file /etc/apt/sources.list.d/${reponame}-${::lsbdistcodename}.list",
      notify  => Exec['aptitude-update'],
      require => Package['python-software-properties'],
  }
  if $key {
    apt::key { $repo: keyid => $key } #Sometimes apt-add-repository fails to get the key.
  }
}