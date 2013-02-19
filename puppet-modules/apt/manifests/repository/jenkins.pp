class apt::repository::jenkins {
  apt::repo { 'jenkins':
    url                    => 'http://pkg.jenkins-ci.org/debian-stable',
    append_lsbdistcodename => false,
    section                => 'binary/'
  }
}
