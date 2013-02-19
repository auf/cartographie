# This class installs vim and a proper config file system-wide
#
# == Parameters
# puppet(boolean):
# if true, will install and activate system-wide vim-puppet
#
# == Variables
#
# == Examples
#
# include vim
#
# == Authors
#
# Bruno Léon <bruno.leon@savoirfairelinux.com>
# Simon Piette <simon.piette@savoirfairelinux.com>
#
# == Copyright
#
# Copyright 2011 Savoir-Faire Linux Inc, unless otherwise noted.
#
class vim (
  $puppet=false
  ) {
  include vim::params
  class { vim::install:
    puppet => $puppet,
  }
  class { vim::config:
    puppet => $puppet,
  }
}

