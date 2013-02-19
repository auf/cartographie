# will create a check for ldap
define shinken::client::ldap::check (
  $check_command,
  $description,
  $service_nagios = $name,
) {
  @@nagios_service { $service_nagios:
    host_name           => $shinken::client::ldap::fqdn,
    check_interval      => undef,
    check_command       => $check_command,
    service_description => $description,
    use                 => $shinken::client::ldap::use,
    tag                 => $shinken::client::ldap::environment,
    servicegroups       => $shinken::client::ldap::extraservicegroup,
    poller_tag          => $shinken::client::ldap::poller_tag,
  }
}
