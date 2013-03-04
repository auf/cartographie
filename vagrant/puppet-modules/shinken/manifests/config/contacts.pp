class shinken::config::contacts (
  $admin_email,
  $admin_paget
){

  @@nagios_contact { 'admin_paget':
    service_notification_options  => 'u,c,r',
    service_notification_period   => '24x7',
    host_notification_options     => 'd,r',
    contactgroups                 => 'administrators,administratorspaget',
    alias                         => 'paget',
    host_notification_period      => '24x7',
    service_notification_commands => 'notify-service-by-email-custom',
    host_notification_commands    => 'notify-host-by-email-custom',
    email                         => "${admin_paget}",
    can_submit_commands           => 1,
  }
  @@nagios_contact { 'admin_email':
    service_notification_options  => 'w,u,c,r,f',
    service_notification_period   => '24x7',
    host_notification_options     => 'd,r',
    contactgroups                 => 'administrators,administratorsemail',
    alias                         => 'email',
    host_notification_period      => '24x7',
    service_notification_commands => 'notify-service-by-email-once',
    host_notification_commands    => 'notify-host-by-email-once',
    email                         => "${admin_email}",
    can_submit_commands           => 1,
  }
  @@nagios_contact { 'probe_email':
    service_notification_options  => 'w,u,c,r,f',
    service_notification_period   => '24x7',
    host_notification_options     => 'd,r',
    alias                         => 'Probe_email',
    host_notification_period      => '24x7',
    service_notification_commands => 'notify-service-by-email-once',
    host_notification_commands    => 'notify-host-by-email-once',
    email                         => "shinken.probe@savoirfairelinux.com",
    can_submit_commands           => 0,
  }

}
