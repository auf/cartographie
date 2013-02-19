class apt::repository::ppa::fabricesp::experimental (
  $stage = pre
  ) {
  apt::ppa { 'ppa_fabricesp_experimental': repo => 'fabricesp/experimental', key => 'F65DB995' }
}
