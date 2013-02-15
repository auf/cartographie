class puppet::config::common {
  concat { $puppet::variables::config_path:
    warn    => true,
  }
  concat { $puppet::variables::auth_config_path:
    warn    => true,
    force   => true,
  }
}
