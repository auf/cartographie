define account::git (
  $home=false,
  $fullname=false,
  $email=false,
  $mergetool=true
) {
  $scope = 'global'
  $gitconfig = "/usr/bin/git config --${scope}"
  $color_settings = [ 'ui', 'diff', 'log', 'status', 'branch' ]

  $username = $name

  if ! $home {
    $userhome = "/home/${username}"
  } else {
    $userhome = $home
  }
  File{
    mode  => 0644,
    owner => $username,
    group => $username,
  }
  Exec{
    user        => $username,
    group       => $username,
    environment => "HOME=${userhome}",
    cwd         => $userhome,
    path        => '/usr/sbin:/usr/bin:/sbin:/bin',
  }

  # Requirements
  # Make sure permissions are fine
  file { "${userhome}/.gitconfig": }
  # To be removed at some point
  file { "${userhome}/.git":
    ensure  => absent,
    force   => true,
  }
  include account::install::git

  if $fullname and $email {
    exec { "${gitconfig} user.email ${email}":
      require => [
        File["${userhome}/.gitconfig"],
        Class['account::install::git'],
      ],
      unless  => "${gitconfig} --get user.email | grep -q ${email}",
    }
    exec { "${gitconfig} user.name \"${fullname}\"":
      require => [
        File["${userhome}/.gitconfig"],
        Class['account::install::git'],
      ],
      unless  => "${gitconfig} --get user.name | grep -q \"${fullname}\"",
    }
    file { "${userhome}/${name}.env":
      ensure  => present,
      content => template('account/user.env'),
    }
  }
}
