define account::vim (
  $home=false
) {
  $username = $title
  File {
    owner => $username,
    mode => 0644,
    group => $name,
  }
  Exec {
    path        => '/usr/sbin:/usr/bin:/sbin:/bin',
    environment => "HOME=$userhome",
    user        => $username,
  }
  include account::install::vim
  # first check for variables
  if $username and $userhome {
    file { "$userhome/.vimrc":
      ensure  => 'present',
      owner   => $username,
      source  => [
        "puppet:///modules/account/${username}/.vimrc",
        "puppet:///modules/account/vimrc"
      ],
      require => Class['account::install::vim'],
    }
    file { [
        "$userhome/.vim",
        "$userhome/.vim/indent",
        "$userhome/.vim/ftplugin",
        "$userhome/.vim/after",
        "$userhome/.vim/after/ftplugin",
      ] :
      ensure => directory,
      mode   => 0755,
    }
    file { "$userhome/.vim/indent/puppet.vim":
      ensure  => 'present',
      source  => "puppet:///modules/account/vim/indent/puppet.vim",
      require => Class['account::install::vim'],
    }
    file { "$userhome/.vim/ftplugin/puppet.vim":
      ensure  => 'present',
      source  => "puppet:///modules/account/vim/ftplugin/puppet.vim",
      require => Class['account::install::vim'],
    }
    file { "$userhome/.vim/after/ftplugin/puppet.vim":
      ensure  => 'present',
      source  => "puppet:///modules/account/vim/after/puppet.vim",
      require => Class['account::install::vim'],
    }
    exec{ "${username}-vim-addons-install-colors":
      command => '/usr/bin/vim-addons install "colors sampler pack"',
      creates => "$userhome/.vim/colors",
      require => Class['account::install::vim'],
    }
    exec{ "${username}-vim-addons-install-puppet":
      command => '/usr/bin/vim-addons install puppet',
      creates => "$userhome/.vim/ftdetect/puppet.vim",
      require => Class['account::install::vim'],
    }
  } else {
    notice("No username and/or userhome specified")
  }
}
