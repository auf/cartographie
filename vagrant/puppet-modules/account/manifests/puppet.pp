define account::puppet (
  $home=false
) {
  $username = $name
  $puppet_envs = '/etc/puppet/environments'
  if ! $home {
    $userhome = $name ? {
      'root'  => '/root',
      default => "/home/${name}"
    }
  } else {
    $userhome = $home
  }

  File {
    mode  => 0644,
    owner => $username,
    group => $username,
  }

  Exec {
    user        => $username,
    group       => $username,
    environment => "HOME=${userhome}",
    path        => '/usr/sbin:/usr/bin:/sbin:/bin',
  }

  file { "${puppet_envs}/${username}":
    recurse      => true,
    recurselimit => 1,
    owner        => $username,
    group        => $username,
    require      => Exec["chown-${username}-puppet"],
  }
  exec { "${username}-puppet-clone":
    command => "git clone ${puppet_envs}/stage ${puppet_envs}/$username",
    user    => 'root',
    creates => "${puppet_envs}/$username/.git",
    require => User[$username],
  }

  exec { "chown-${username}-puppet":
    command => "chown -R ${username}:${username} ${puppet_envs}/${username}",
    user    => 'root',
    require => Exec["${username}-puppet-clone"],
    unless  => [
      "stat -c %U:%G ${puppet_envs}/${username}/.git | grep -q ^${username}:${username}$",
      "stat -c %U:%G ${puppet_envs}/${username}/site | grep -q ^${username}:${username}$",
      "stat -c %U:%G ${puppet_envs}/${username}/modules | grep -q ^${username}:${username}$",
    ],
  }

  exec { "${username}-git-hooks":
    command => "${puppet_envs}/${username}/.hooks/install",
    cwd     => "${puppet_envs}/${username}",
    creates => "${puppet_envs}/${username}/.git/hooks/pre-commit",
    require => File["${puppet_envs}/${username}"],
  }

  # only fetch master from stage
  exec { "${username}-git-remote-fetch":
    command => 'git config remote.origin.fetch +refs/heads/master:refs/remotes/origin/master',
    cwd     => "${puppet_envs}/$username",
    unless  => 'git config remote.origin.fetch | grep -q ^+refs/heads/master:refs/remotes/origin/master$',
    require => File["${puppet_envs}/${username}"],
  }

  # always push the local master branch under the name ${username} on stage repo
  exec { "${username}-git-remote-push":
    command => "git config remote.origin.push +refs/heads/master:refs/heads/${username}",
    cwd     => "${puppet_envs}/$username",
    unless  => "git config remote.origin.push | grep -q ^+refs/heads/master:refs/heads/${username}$",
    require => File["${puppet_envs}/${username}"],
  }
}
