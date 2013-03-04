class apt::repository::ppa::kubuntu::ppa (
  $stage = pre
  ) {
  apt::ppa { 'ppa_kubuntu-ppa': repo => 'kubuntu-ppa/ppa', key => '8AC93F7A'}
}

class apt::repository::ppa::kubuntu::backports (
  $stage = pre
  ) {
  apt::ppa { 'ppa_kubuntu-backports': repo => 'kubuntu-ppa/backports', key => '8AC93F7A'}
}
