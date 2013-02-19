class apt::repository::ppa::sevenmachines::flash (
  $stage = pre
  ) {
  apt::ppa { 'ppa_sevenmachines-flash': repo => 'sevenmachines/flash', key => '61E46227'}
}