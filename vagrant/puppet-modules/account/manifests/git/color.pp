define account::git::color ($scope='global', $value='auto') {
  $gitconfig = $account::git::gitconfig
  exec { "${gitconfig} ${name}.color ${value}":
    unless      => "${gitconfig} --get ${name}.color | grep -q ${value}",
  }
}
