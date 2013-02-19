define account::profile (
  $site
) {
  $username = $title
  if ! $home {
    $home = "/home/${username}"
  }
  file { $home:
    path    => $home,
    recurse => 'remote',
    source  => "puppet:///modules/${site}/profiles/${username}",
    owner   => $username,
    group   => $username,
    mode    => '0755',
  }
}
