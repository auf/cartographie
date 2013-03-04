class apt::repository::ppa::blt04 (
  $stage = pre
  ) {
  apt::ppa { 'ppa_blt04': repo => 'blt04/ppa', key => 'D4998A22'}
}
