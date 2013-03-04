# * Install any modules indicated as required
# * Create the doc root, log folder etc...
#
# == Parameters
#
# A lot of standard Apache configuration file parameters not described below are also usable. They are prefixed with apache2_ (ex: DirectoryIndex => $apache2_directory_index)
#
# $client :: The client this website belongs to
# $site_domain :: The domain of the website
# site_ips :: Addresses on Listen 80
# site_ips_ssl :: Addresses on Listen 443
# $confname :: The website name ( www.yahoo.fr => confname is 'www')
# $required_modules :: The list of modules required by the website
# $source :: If specified, the site configuration will be taken from Puppet filserver [ "puppet:///modules/apache2/client/domain/${source}", "puppet:///modules/apache2/client/${source}" ]
# $template :: The puppet path to the template this website should be generated from
# $load_order :: If specified, the link in sites-enabled will be prepended by this value to influence Apache2 order of configurations loading
# $force_ssl (false #*true*|*force*):: When this site is accessible in SSL. If set to force, HTTP traffic will be redirected to HTTPS.
# $proxy_from_to :: The proxy string used as ProxyPass / ProxyPassReverse
# $has_awstats :: Whether configuration for awstats statistics generation should be created for this website
# $jkmountfile :: Specify the path to mod_jk mount_file when using mod_jk
# $apache2_aliases ([]) :: The list of aliases this website should respond to. Elements will be appended $domain
# $apache2_fqdnaliases ([]) :: The list of fqdn aliases this website should respond to. Elements will not be appended $domain
# $apache2_specific ([]) :: This allow you to provide a list of strings that will be added to your config
define apache2::website(
  $ensure                         = 'present',
  $apache2_admin_email            = "webmaster@${domain}",
  $client                         = undef,
  $confname                       = inline_template('<%= name.split(".")[0] %>'),
  $site_domain                    = inline_template('<%= name.split(".")[1..-1].join(".") %>'),
  $site_ips                       = '*',
  $site_ips_ssl                   = false,
  $required_modules               = false,
  $create_document_root           = true,
  $config_source                  = false,
  $config_template                = 'apache2/website.erb',
  $load_order                     = undef,
  $ensure                         = 'present',
  $website_owner                  = 'root',
  $website_group                  = 'root',
  $force_ssl                      = false,
  $has_ssl_ca                     = false,
  $proxy_from_to                  = false,
  $has_cgi                        = false,
  $has_awstats                    = false,
  $jkmountfile                    = false,
  $apache2_aliases                = false,
  $apache2_fqdnaliases            = false,
  $apache2_document_root_override = undef,
  $apache2_directory_index        = false,
  $apache2_alias                  = false,
  $apache2_aliasmatch             = false,
  $apache2_scriptalias            = false,
  $apache2_includes               = false,
  $apache2_options                = ['Indexes', 'FollowSymLinks', 'MultiViews'],
  $apache2_allowoverride          = ['None'],
  $apache2_order                  = 'deny,allow',
  $apache2_allow_from             = 'all',
  $apache2_deny_from              = 'all',
  $apache2_specific               = false,
  $apache2_rootdirectory_specific = false,
  $apache2_error_log_override     = undef,
  $apache2_custom_log_override    = undef,
  $documentroot_source            = false,
  $apache2_ssl_proxy_engine       = false,
#Allows for Authentication using file
  $authuserfile                   = false,
  $authfilename                   = 'Authentication Required',
  $file_auth_require              = ['valid-user'],
#Allows for LDAP based Authentication
  $authldapurl                    = false,
  $authldapname                   = 'Authentication Required',
  $authldapbinddn                 = false,
  $authldapbindpassword           = false,
  $ldap_auth_require              = ['valid-user'],
  $monitor                        = false,
  $nagios_service_template        = 'Template_Service_Base',
  $nagios_contacts                = 'dummy',
  $nagios_contact_groups          = 'dummy',
  $nagios_notification_period     = '24x7',
  $nagios_servicegroups           = '+Web',
  $website_backup                 = false
  ) {

  # Dependencies to other resources
  include apache2::variables

  Class['apache2'] -> Apache2::Website[$name] ~> Exec['reload-apache2']

  if $site_ips_ssl {
    realize Apache2::Module['ssl']

    #We remap default-ssl to default to avoid the need for default-ssl SSL declarations all around
    if $confname == 'default-ssl' {
      Ssl::Config::Apache2['default'] -> Apache2::Website[$name]
    }
    else {
      Ssl::Config::Apache2[$name] -> Apache2::Website[$name]
    }
  }

  if $force_ssl {
    if ! $site_ips_ssl {
      fail("You cannot force SSL without any \$site_ips_ssl for ${name}" )
    }
    realize Apache2::Module['rewrite']
  }

  if $proxy_from_to {
    realize Apache2::Module['proxy_http']
  }

  if $required_modules {
    realize Apache2::Module[$required_modules]
  }

  if $authldapurl {
    realize Apache2::Module['ldap', 'authnz_ldap']
  }

  # BUG 6710 prevent this
  #  if $apache2_includes {
  #    File[$apache2_includes] -> Apache2::Website[$name]
  #  }

  # Variables used throughout this manifest
  case $apache2::my_apache2_hierarchical_organisation {
    true: {
      $hierarchical_folder_path = $apache2::my_apache2_separate_clients ? {
        true  => "${client}/${site_domain}",
        false => $site_domain,
      }
      $file_path_suffix         = $confname

    }
    false: {
      $hierarchical_folder_path = undef
      $file_path_suffix = "${site_domain}_${confname}"
    }
  }

 $website_conf_file   = $confname ? {
    'default'     => "${apache2::variables::apache_root_path}/sites-available/${load_order}${confname}",
    'default-ssl' => "${apache2::variables::apache_root_path}/sites-available/${load_order}${confname}",
    default       => regsubst( "${apache2::variables::apache_root_path}/sites-available/${hierarchical_folder_path}/${load_order}${file_path_suffix}", '//', '/' ),
  }
  $apache2_document_root = $apache2_document_root_override ? {
    undef   => regsubst( "${apache2::variables::apache_doc_path}/${hierarchical_folder_path}/${file_path_suffix}", '//', '/' ),
    default => $apache2_document_root_override,
  }
  $apache2_error_log = $apache2_error_log_override ? {
    undef   => regsubst( "${apache2::variables::apache_log_path}/${hierarchical_folder_path}/${file_path_suffix}_error.log", '//', '/' ),
    default => $apache2_error_log_override,
  }
  $apache2_custom_log = $apache2_custom_log_override ? {
    undef   => regsubst( "${apache2::variables::apache_log_path}/${hierarchical_folder_path}/${file_path_suffix}_access.log combined_with_deflate_ratio", '//', '/' ),
    default => $apache2_custom_log_override,
  }

  if ( $apache2::my_apache2_hierarchical_organisation ) and ( $confname != 'default' ) and ( $confname != 'default-ssl' ) {
    if ( $apache2::my_apache2_separate_clients ) and ( ! defined( Apache2::Hierarchical::Client[ $client ] ) ) {
      apache2::hierarchical::client { $client:
        client => $client,
      }
    }
    if ! defined( Apache2::Hierarchical::Domain[ $site_domain ] ) {
      apache2::hierarchical::domain { $site_domain:
        hierarchical_folder_path => $hierarchical_folder_path
      }
    }
  }

  if $create_document_root {
    file { $apache2_document_root:
      ensure    => directory,
      mode      => '0755',
      owner     => $website_owner,
      group     => $website_group,
    }
  }

  if ( $config_source ) and ( $config_template ) {
    #This would fail on below File resources anyway, but makes it mor clear than a duplicate error msg
    fail ( 'You must provide either a source config file or a template to generate one, not both' )
  }

  if $config_source {
    file { $website_conf_file:
      ensure  => file,
      mode    => '0644',
      source  => $config_source,
    }
  }
  elsif $config_template {
    file { $website_conf_file:
      ensure  => file,
      mode    => '0644',
      content => template($config_template),
    }
  }
  else {
    fail ('You must provide either a source config file or a template to generate one')
  }

  file { "Website_${name}":
    path        => $confname ? {
      'default'     => "${apache2::variables::apache_root_path}/sites-enabled/000default",
      'default-ssl' => "${apache2::variables::apache_root_path}/sites-enabled/004default-ssl",
      default       => "${apache2::variables::apache_root_path}/sites-enabled/$load_order${site_domain}_${confname}",
    },
    target  => $website_conf_file,
    ensure  => $ensure? {
      /(link|present)/  => link,
      default           => absent,
    },
    mode    => '0644',
    require => File[$website_conf_file],
  }

  case $site_ips {
    #If we bind on all IP apache has been confgured to Listen on, the only thing we can check is that
    #at least one binding has been declared
    '*': {
      if ! $apache2::my_apache2_listen_ips {
        fail('You are trying to declare a website but Apache is not configured to Listen on any HTTP port')
      }
      realize Apache2::Namevirtualhost [ $site_ips ]
    }
    false: {}
    default: {
      if ! $apache2::my_apache2_listen_ips {
        fail('You are trying to declare a website but Apache is not configured to Listen on any HTTP port')
      }
      realize Apache2::Namevirtualhost [ $site_ips ]
    }
    # Bug 6710 prevent this for now. Will be fine then though
    #default: Apache2::Bindipaddress[$site_ips] -> Website[$name]
  }

  case $site_ips_ssl {
    #If we bind on all IP apache has been confgured to Listne on, the only thing we can check is that
    #at least one binding has been declared
    '*': {
      if ! $apache2::my_apache2_listen_ips_ssl {
        fail('You are trying to declare an SSL website but Apache is not configured to Listen on any HTTPS port')
      }
      realize Apache2::Namevirtualhost::Ssl [ $site_ips ]
    }
    false: {}
    default: {
      if ! $apache2::my_apache2_listen_ips_ssl {
        fail('You are trying to declare an SSL website but Apache is not configured to Listen on any HTTPS port')
      }
      realize Apache2::Namevirtualhost::Ssl [ $site_ips ]
    }
  }
}
