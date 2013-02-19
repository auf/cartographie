class shinken::install {
  include shinken::variables
  
  package { $shinken::variables::packages:
     ensure => present
  }
  
  concat { $shinken::variables::configfile:
    warn    => "#This file is managed by Puppet. DO NOT EDIT MANUALLY\n"
  }
}
