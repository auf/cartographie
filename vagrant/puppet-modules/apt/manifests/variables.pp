class apt::variables {
  $apt_dir          = '/etc/apt'
  $apt_sources_dir  = "${apt_dir}/sources.list.d"
  $apt_conf_dir     = "${apt_dir}/apt.conf.d"
  $apt_section = $::lsbdistid ? {
    Debian => 'main contrib non-free',
    Ubuntu => 'main restricted universe multiverse'
  }
}
