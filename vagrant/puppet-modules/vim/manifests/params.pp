class vim::params {
  if $::osfamily == 'Debian' {
    $pkgs     = [ 'vim', 'vim-scripts', 'vim-addon-manager' ]
    $basepath = '/etc/vim'
  }
  elsif $::osfamily == 'RedHat' {
    $pkgs     = 'vim-enhanced'
    $basepath = '/etc/'  
  }
  else {
    fail('Unsupported operating system')
  }
}
