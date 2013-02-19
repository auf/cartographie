define apache2::bindipaddress::requirehack (
  $website_name,
  $ssl
  ) {
  if $ssl {
    Apache2::Bindipaddress::Ssl[$name] -> Website[$website_name]
  }
  else {
    Apache2::Bindipaddress[$name] -> Website[$website_name]
  }
}
