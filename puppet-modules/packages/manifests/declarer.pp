define packages::declarer() {
  if ! $packages::packageshash[$name] {
    $pkgname = $name
  } else {
    $pkgname = $packages::packageshash[$name]
  }

  if (! defined(Package[$name])) {
    @package { $name:
      ensure  => present,
      name    => $pkgname,
    }
  }
}
