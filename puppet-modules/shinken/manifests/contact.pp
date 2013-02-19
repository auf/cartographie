define shinken::contact (
  $username = $name,
  $service_notification_options = "wucr",
  $service_notification_period = "WorkHours",
  $host_notification_options = "dur",
  $host_notification_period = "WorkHours",
  $contactgroups = "administrators",
  $email = "nobody",
  $service_notification_commands = "notify-service-by-email-custom",
  $host_notification_commands = "notify-host-by-email-custom",
  $can_submit_commands = 1,
  $host_notifications_enabled = 0,
  $service_notifications_enabled = 0,
  $ensure = present,
){
  @@nagios_contact { $username:
    service_notification_options  => $service_notification_options,
    service_notification_period   => $service_notification_period,
    host_notification_options     => $host_notification_options,
    host_notification_period      => $host_notification_period,
    contactgroups                 => $contactgroups,
    service_notification_commands => $service_notification_commands,
    host_notification_commands    => $host_notification_commands,
    email                         => $email,
    ensure                        => $ensure,
    can_submit_commands           => $can_submit_commands,
    host_notifications_enabled    => $host_notifications_enabled,
    service_notifications_enabled => $service_notifications_enabled,
  }
}

