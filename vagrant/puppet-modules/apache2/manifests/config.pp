# do not use directly
class apache2::config (
  $apache2_admin_email,
  $apache_info_allowed,
  $apache2_listen_ips,
  $apache2_listen_ips_ssl,
  $monitor,
  $nagios_service_template,
  $nagios_contacts,
  $nagios_contact_groups,
  $nagios_notification_period,
  $nagios_servicegroups,
  $defaultwebsites_classname
  ) {

  include apache2::variables

  # Make the variables available for websites
  $my_apache2_listen_ips     = $apache2_listen_ips
  $my_apache2_listen_ips_ssl = $apache2_listen_ips_ssl


  $default_mode  =  $::osfamily ? {
    'Debian'   => '0750',
    'RedHat'   => '0700',
  }
  file { $apache2::variables::apache_log_path:
    ensure  => directory,
    owner   => root,
    group   => $apache2::variables::apache_log_group,
  }

  if $::osfamily == 'RedHat' {
    file { "${apache2::variables::apache_root_path}/conf/httpd.conf":
      ensure  => file,
      mode    => '0644',
      source  => 'puppet:///modules/apache2/httpd_redhat.conf',
    }

    file { "${apache2::variables::apache_root_path}/mods-available":
      ensure  => directory,
      mode    => '0755',
    }

    file { "${apache2::variables::apache_root_path}/mods-enabled":
      ensure  => directory,
      purge   => true,
      recurse => true,
      mode    => '0755',
    }

    file { '/var/lock/httpd':
      ensure  => directory,
      mode    => '0755',
      owner   => $apache2::variables::apache_user,
    }

    file { [
      "${apache2::variables::apache_root_path}/conf.d/proxy_ajp.conf",
      "${apache2::variables::apache_root_path}/conf.d/welcome.conf",
      "${apache2::variables::apache_root_path}/conf.d/README"
      ]:
      ensure  => absent,
    }
  }

  file { $apache2::variables::apache_doc_path:
    ensure  => directory,
    links   => follow,
    mode    => '0755',
  }

  file { "${apache2::variables::apache_root_path}/sites-available":
    ensure  => directory,
    mode    => '0755',
  }

  file { "${apache2::variables::apache_root_path}/sites-enabled":
    ensure  => directory,
    mode    => '0755',
    purge   => true,
    recurse => true,
    force   => true,
  }

  file { "${apache2::variables::apache_root_path}/specific-includes":
    ensure  => directory,
    mode    => '0755',
    purge   => true,
    recurse => true,
    force   => true,
  }

  file { "${apache2::variables::apache_root_path}/conf.d/improvments.conf":
    ensure  => present,
    source  => 'puppet:///modules/apache2/improvments.conf',
  }

  concat { '/etc/apache2/ports.conf':
    owner   => root,
    group   => root,
    mode    => '0644',
    warn    => true,
  }

  if ! $apache2_listen_ips and ! $apache2_listen_ips_ssl {
    fail('Apache does not allow to be started without a Listen directive. Please adjust your apache2_listen_ips{_ssl} directives')
  }

  @apache2::namevirtualhost { '*': }
  case $apache2_listen_ips {
    false: { }
    '*': {
      apache2::bindipaddress   { '*': }
    }
    default: {
      apache2::bindipaddress   { $apache2_listen_ips: }
      @apache2::namevirtualhost { $apache2_listen_ips: }
    }
  }

  @apache2::namevirtualhost::ssl { '*': }
  case $apache2_listen_ips_ssl {
    false: { }
    '*': {
      apache2::bindipaddress::ssl   { '*': }
      realize Apache2::Website['default-ssl']
    }
    default: {
      apache2::bindipaddress::ssl   { $apache2_listen_ips_ssl: }
      @apache2::namevirtualhost::ssl { $apache2_listen_ips_ssl: }
      realize Apache2::Website['default-ssl']
    }
  }

  realize Apache2::Module['alias', 'auth_basic', 'auth_digest', 'authn_file', 'authz_host', 'authz_user', 'deflate', 'dir', 'info', 'mime', 'negotiation', 'status', 'setenvif']

  #Those are builtin in Debian
  if $::osfamily == 'RedHat' {
    realize Apache2::Module['log_config', 'logio']
  }

  if $defaultwebsites_classname {
    include $defaultwebsites_classname
  }
}
