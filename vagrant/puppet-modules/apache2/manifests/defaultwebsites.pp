class apache2::defaultwebsites {
  apache2::website { "default":
    site_domain          => $::domain, #Must be passed because $name is not FQDN so $site_domain cannot be discovered
    load_order           => '000',
    config_template      => 'apache2/website-default.erb',
    has_awstats          => false,
    monitor              => false,
    create_document_root => false,
  }

  if $apache2::apache2_listen_ips_ssl {
    apache2::website { "default-ssl":
      site_domain          => $::domain, #Must be passed because $name is not FQDN so $site_domain cannot be discovered
      load_order           => '004',
      config_template      => 'apache2/website-default.erb',
      has_awstats          => false,
      monitor              => false,
      site_ips_ssl         => '*',
      create_document_root => false,
    }
  }
}

