#puppet apply --modulepath=/etc/puppet/environments/development/modules /etc/puppet/environments/development/modules/puppet/tests/server.pp

if ! $::fqdn {
  fail('Please setup machine fqdn properly.')
}
stage { pre:
  before => Stage[main],
}

Exec {
  path  => '/usr/bin:/bin:/usr/sbin:/sbin',
}
File {
  owner => 'root',
  group => 'root',
}

include packages

class { 'puppet::client':
  certname => $certname
}

class { 'puppet::master':
  use_passenger => true,
}

class { 'puppet::db': }

class { 'apache2':
  monitor => false,
}

apache2::website { "puppet${location}.${domain}":
  confname              => "puppet${location}",
  config_template       => 'apache2/website-puppet.erb',
  required_modules      => ['passenger', 'ssl'],
  create_document_root  => false,
  has_awstats           => false,
  monitor               => false,
  require               => Class['puppet::master::passenger::install']
}
