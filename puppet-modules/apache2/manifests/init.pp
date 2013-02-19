# = Class: apache2
#
# * Install apache2 and configure default websites
# * _INFO_: Default domain is the host domain_
# == Parameters
#
# $websites_owner (root):: Owner of apache2 websites folder
# $websites_group (root):: Group of apache2 websites folder
# $apache_info_allowed ([localhost]):: IP list with access to webserver info provided by mod_info
class apache2 (
  $apache2_admin_email        = "webmaster@${domain}",
  $apache_info_allowed        = [ 'localhost', 'localhost.localdomain', $::fqdn ],
  $apache2_listen_ips         = '*',
  $apache2_listen_ips_ssl     = false,
  $monitor                    = false,
  $nagios_service_template    = 'Template_Service_Base',
  $nagios_contacts            = 'dummy',
  $nagios_contact_groups      = 'dummy',
  $nagios_notification_period = false,
  $nagios_servicegroups       = '+Web',
  $defaultwebsites_classname  = 'apache2::defaultwebsites',
  $separate_clients           = false,
  $hierarchical_organisation  = false
) {

  include apache2::variables

  # Make the variables available for websites. The define depends on this class
  # So there should be no parse order issue
  $my_apache2_listen_ips     = $apache2_listen_ips
  $my_apache2_listen_ips_ssl = $apache2_listen_ips_ssl
  $my_apache2_hierarchical_organisation = $hierarchical_organisation
  $my_apache2_separate_clients          = $separate_clients

  class { 'apache2::install': } -> Class['apache2::config'] ~> class { 'apache2::service': }

  class { 'apache2::config':
    apache2_admin_email        => $apache2_admin_email,
    apache_info_allowed        => $apache_info_allowed,
    apache2_listen_ips         => $apache2_listen_ips,
    apache2_listen_ips_ssl     => $apache2_listen_ips_ssl,
    monitor                    => $monitor,
    nagios_service_template    => $nagios_service_template,
    nagios_contacts            => $nagios_contacts,
    nagios_contact_groups      => $nagios_contact_groups,
    nagios_notification_period => $nagios_notification_period,
    nagios_servicegroups       => $nagios_servicegroups,
    defaultwebsites_classname  => $defaultwebsites_classname
  }
  class { 'apache2::modulespredeclaration': }

  realize Apache2::Module['alias', 'auth_basic', 'auth_digest', 'authn_file', 'authz_host', 'authz_user', 'deflate', 'dir', 'info', 'mime', 'negotiation', 'status', 'setenvif']

  #Those are builtin in Debian
  if $::osfamily == 'RedHat' {
    realize Apache2::Module['log_config', 'logio']
  }

  if $monitor == true {
    if $nagios_contacts == 'dummy' and $nagios_contact_groups == 'dummy' {
      fail('You must provide either $nagios_contacts / $nagios_contact_groups or both')
    }

    @@nagios_service { "Apache2_${::hostname}":
      use                 => $nagios_service_template,
      check_command       => 'check_nrpe!check_apache2',
      service_description => 'Apache2',
      servicegroups       => '+Web',
      notification_period => $nagios_notification_period,
      tag                 => $::environment
    }
  }
}

