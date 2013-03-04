class apt::repository::ppa::clamav (
  $stage = pre
  ) {
  apt::ppa { 'ppa_clamav': repo => 'ubuntu-clamav/ppa', key => '5ADC2037' }
}
