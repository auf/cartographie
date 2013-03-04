class { 'apache2': }

apache2::website { 'www.example.com': }

apache2::website { 'gosa.example.com':
  required_modules                => ['php5'],
  apache2_document_root_override  => '/usr/share/gosa/html',
  apache2_includes                => ['/etc/gosa/gosa-apache.conf'],
  site_ips_ssl                    => '*',
  force_ssl                       => force
}