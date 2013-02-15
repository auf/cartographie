class packages {
  case $osfamily {
    'RedHat': {
      $libdbd_mysql_perl  = 'perl-DBD-MySQL'
      $libdbi_perl        = 'libdbi-dbd-mysql'
      $phpmssql           = 'php-mssql'
      $phpxml             = 'php-xml'
      $python_memcache    = 'python-memcached'
      $sysvinit_utils     = 'sysvinit-tools'
    }
    'Debian': {
      $libactiverecord_ruby = 'libactiverecord-ruby'
      $libmysql_ruby        = 'libmysql-ruby'
      $phpmssql             = 'php5-sybase'
      $phpxml               = 'php5-xml'
    }
    default: {
      fail('Unsupported osfamily')
    }
  }

  $packageshash = {
    'libactiverecord-ruby'     => $libactiverecord_ruby,
    'libapache2-mod-jk'        => $libapache2_mod_jk,
    'libapache2-mod-passenger' => $libapache2_mod_passenger,
    'libapache2-mod-php5'      => $libapache2_mod_php5,
    'libapache2-svn'           => $libapache2_svn,
    'libdbd-mysql-perl'        => $libdbd_mysql_perl,
    'libdbi-perl'              => $libdbi_perl,
    'libmysql-ruby'            => $libmysql_ruby,
    'php-cli'                  => $php_cli,
    'php-pear'                 => $php_pear,
    'php5'                     => $php5,
    'php5-cli'                 => $php5_cli,
    'php5-gd'                  => $php5_gd,
    'php5-mcrypt'              => $php5_mcrypt,
    'php5-mysql'               => $php5_mysql,
    'python-memcache'          => $python_memcache,
    'rails'                    => $rails,
    'sysstat'                  => $sysstat,
    'sysvinit-utils'           => $sysvinit_utils,
  }

  #Convert the hash keys into an array so we can pass it to a define
  $keys = keys( $packageshash )

  #Call the define with the generated array
  packages::declarer { $keys : }
}

