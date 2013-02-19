ssl::key { 'wildcard.example.com':
  source => 'puppet:///files/example.com/certs/wildcard.example.com.key',
}
ssl::cert { 'wildcard.example.com':
  source => 'puppet:///files/example.com/certs/wildcard.example.com.crt',
}
ssl::chain { 'wildcard.example.com':
  source => 'puppet:///files/example.com/chains/wildcard.example.com.chain',
}

ssl::config::apache2 { 'wildcard.example.com':
  tls_key   => 'wildcard.example.com',
  tls_chain => 'wildcard.example.com',
}

ssl::config::apache2 { 'www.example.com':
  link_to => 'wildcard.example.com',
}
