class vim::config (
  $puppet = false
  ) {
  include vim::params
  file { "${vim::params::basepath}/vimrc.local":
    ensure  => present,
    source  => 'puppet:///modules/vim/vimrc.local',
    require => Class['vim::install'],
  }
  if $osfamily == 'Debian' {
    # for now vim-add-install-colors only works on Ubuntu Lucid and later
    if $lsbdistid == 'Ubuntu' and $lsbdistrelease == '8.04' {
      file { '/var/lib/vim/addons/colors':
        ensure  => link,
        target  => '/usr/share/vim-scripts/colors',
        require => Class['vim::install'],
      }
    } else {
      exec { "vim-addons-install-colors":
        user        => 'root',
        environment => 'HOME=/root',
        command     => "/usr/bin/vim-addons install -w 'colors sampler pack'",
        creates     => "/var/lib/vim/addons/plugin/color_sample_pack.vim",
        require     => Class['vim::install'],
      }
    }
    if $puppet {
      exec{ "vim-addons-install-puppet":
        user        => 'root',
        environment => 'HOME=/root',
        command     => '/usr/bin/vim-addons install -w puppet',
        creates     => "/var/lib/vim/addons/syntax/puppet.vim",
        require     => Class['vim::install'],
      }
      file { '/var/lib/vim/addons/after/':
        ensure  => directory,
        require => Exec['vim-addons-install-puppet'],
      }
      file { "/var/lib/vim/addons/after/puppet.vim":
        ensure  => 'present',
        source  => "puppet:///modules/vim/after.puppet.vim",
        require => [
          File['/var/lib/vim/addons/after'],
          Class['vim::install'],
        ],
      }
    }
  }
}
