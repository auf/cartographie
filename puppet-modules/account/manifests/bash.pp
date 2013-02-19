define account::bash (
  $home=false
) {
  File{
    mode  => 0644,
    owner => $name,
    group => $name,
  }
  if ! $username {
    $username = $name
  }
  if ! $home {
    $userhome = "/home/${username}"
  } else {
    $userhome = $home
  }
  include account::install::bash
  file { "${userhome}/.bashrc":
    ensure  => 'present',
    source  => [
      "puppet:///modules/account/${username}/.bashrc",
      'puppet:///modules/account/bashrc',
    ],
    require => Class['account::install::bash'],
  }
  file { "${userhome}/.profile":
    ensure  => 'present',
    source  => [
      "puppet:///modules/account/${username}/.profile",
      'puppet:///modules/account/profile',
    ],
    require => Class['account::install::bash'],
  }
}
