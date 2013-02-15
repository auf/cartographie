exec { "apt-update":
    command => "/usr/bin/apt-get update"
}

Exec["apt-update"] -> Package <| |>

package {
  "build-essential": ensure => installed;
  "python": ensure => installed;
  "python-dev": ensure => installed;
  "python-setuptools": ensure => installed;
  # "python-pip": ensure => installed;
  # "python-virtualenv": ensure => installed;
  "python-mysqldb": ensure => installed;
  # "python-imaging": ensure => installed;
  # "git": ensure => installed;
  # "xsltproc": ensure => installed;
  # "libxslt1-dev": ensure => installed;
  # "mysql-client": ensure => installed;
}

class { 'sudo':
  nopasswd => true
}

class {'mysql::server': }

# bd de l'app
mysql_database { 'cartographie':
  ensure => present;
}

# bd pour les references
mysql_database { 'datamaster':
  ensure => present;
}

mysql::user { 'root' :
  ensure => present,
  require  => Service['mysql'],
  password => 'root',
  host     => 'localhost'
}

mysql::rights::standard { 'root' :
  database => 'cartographie',
  user     => 'root',
  host     => 'localhost',
}