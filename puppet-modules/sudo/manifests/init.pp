class sudo (
  $nopasswd = false
  ) {
  include sudo::params
  include sudo::config
}
