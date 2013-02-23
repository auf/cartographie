class sudo::params {
  if ! $ec2_instance_id or $sudo::nopasswd {
    $basefileurl = 'puppet:///modules/sudo/sudoers_base_nopasswd'
  } else {
    $basefileurl = 'puppet:///modules/sudo/sudoers_base'
  }
}

