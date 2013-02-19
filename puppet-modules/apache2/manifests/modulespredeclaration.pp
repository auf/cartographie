# do not use this class directly
class apache2::modulespredeclaration {
  @apache2::module { 'actions':     }
  @apache2::module { 'alias':       }
  @apache2::module { 'auth_basic':  }
  @apache2::module { 'auth_digest': }
  @apache2::module { 'authn_file':  }
  @apache2::module { 'authz_host':  }
  @apache2::module { 'authz_user':  }
  @apache2::module { 'authnz_ldap': }
  @apache2::module { 'cgi':         }
  @apache2::module { 'dav':         }
  @apache2::module { 'dav_svn':
    required_package => ['libapache2-svn']
  }
  @apache2::module { 'deflate':
    base_config => true,
    config      => 'source'
  }
  @apache2::module { 'dir':
    base_config => true
  }
  @apache2::module { 'env':
    ensure => 'present'
  }
  @apache2::module { 'headers':
    ensure => 'present'
  }
  @apache2::module { 'info':
    config => 'template'
  }
  @apache2::module { 'jk':
    required_package  => ['libapache2-mod-jk'],
    config            => 'template'
  }
  @apache2::module { 'log_config': }
  @apache2::module { 'logio':
    ensure => 'present'
  }
  @apache2::module { 'ldap':
    ensure => 'present'
  }
  @apache2::module { 'mime':
    base_config => true
  }
  @apache2::module { 'negotiation':
    base_config => true }
  @apache2::module { 'passenger':
    required_package  => ['libapache2-mod-passenger'],
    config            => 'template'
  }

  case $::osfamily {
    'RedHat': {
      $php5_packages_list = [ 'php', 'php-cli' ]
      $module_real_name   = 'libphp5'
    }
    'Debian': {
      $php5_packages_list = [ 'php5', 'php5-cli', 'libapache2-mod-php5' ]
      $module_real_name   = 'php5'
    }
    default: {
      fail('Unsupported OS family')
    }
  }
  @apache2::module { 'php5':
    ensure            => 'present',
    required_package  => $php5_packages_list,
    module_real_name  => $module_real_name,
    config            => 'source'
  }
  @apache2::module { 'proxy':      }
  @apache2::module { 'proxy_http': }
  @apache2::module { 'rewrite':    }
  @apache2::module { 'setenvif':
    base_config => true
  }
  @apache2::module { 'speling':    }
  @apache2::module { 'ssl':        }
  @apache2::module { 'status':
    config => 'template'
  }
}

