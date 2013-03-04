class sudo::config (
  $basefileurl = $sudo::params::basefileurl
) {
  include concat::setup

  concat { '/etc/sudoers':
    owner   => root,
    group   => root,
    mode    => 0440,
  }

  concat::fragment{ 'sudoers_base':
    target  => '/etc/sudoers',
    order   => 01,
    source  => $basefileurl,
  }
}

