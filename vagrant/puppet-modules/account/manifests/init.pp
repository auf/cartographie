define account (
  $email,
  $fullname,
  $ensure=present,
  $shell='/bin/bash',
  $groups=[],
  $vim=false,
  $bash=false,
  $git=false,
  $rmhome=false,
  $profile=false,
  $puppet=false,
  $site=false,
  $ssh_key_ensure=present,
  $ssh_key=false,
  $ssh_keytype=false,
  $ssh_name=false
) {
  $username = $title
  $userhome = "/home/${title}"
  user { $username:
    ensure     => $ensure,
    comment    => $fullname,
    shell      => $shell,
    home       => $userhome,
    groups     => $groups,
    managehome => true,
  }
  if $ensure == 'absent' {
    if $rmhome == true {
      file { $userhome:
        ensure => absent,
        force  => true,
      }
    }
    if $puppet {
      if $username {
        exec { "rm ${username}-puppet":
          command => "rm -rf /etc/puppet/environments/${username}",
          onlyif  => "ls -ld /etc/puppet/environments/${username}",
        }
      }
    }
  }
  if $ensure == present {
    if $puppet {
      account::puppet { $username: }
    }
    if $profile {
      if ! $site {
        fail('account: site parameter have to be defined when profile is used.')
      }
      account::profile { $username:
        site => $site,
      }
    }
    if $git {
      account::git { $username:
        fullname => $fullname,
        email    => $email,
      }
    }
    if $ssh_key {
      ssh_authorized_key { "${username}-${ssh_name}":
        ensure  => present,
        user    => $username,
        type    => $ssh_keytype,
        key     => $ssh_key,
        name    => $ssh_name,
      }
    }
  }
}
