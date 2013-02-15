class puppet::client::install (
 $lightclient = false,
)  {
  if ! $lightclient {
    package { $puppet::variables::client_packages:
      ensure => present
    }
  }
}
