class shinken::config::notificationcommands {
  nagios_command { 'notify-host-by-email-custom':
    command_line => '/usr/bin/printf "%b" "***** Nagios *****\n\nNotification Type: $NOTIFICATIONTYPE$\nHost: $HOSTNAME$\nState: $HOSTSTATE$\nAddress: $HOSTADDRESS$\nInfo:\n\n$HOSTOUTPUT$ $LONGHOSTOUTPUT$\n\nDate/Time: $LONGDATETIME$\n\nLink : https://monitoring.savoirfairelinux.com/thruk/cgi-bin/status.cgi?host=$HOSTNAME$\n\n Client : $HOSTNOTES$\n" | /usr/bin/mail -s "** $NOTIFICATIONTYPE$ Host Alert: $HOSTNAME$ is $HOSTSTATE$ **" $CONTACTEMAIL$'
  }
  nagios_command { 'notify-service-by-email-custom':
    command_line => '/usr/bin/printf "%b" "***** Nagios *****\n\nNotification Type: $NOTIFICATIONTYPE$\n\nService: $SERVICEDESC$\nHost: $HOSTALIAS$\nAddress: $HOSTADDRESS$\nState: $SERVICESTATE$\n\nDate/Time: $LONGDATETIME$\n\nAdditional Info:\n\n$SERVICEOUTPUT$ $LONGSERVICEOUTPUT$\n\nLink : https://monitoring.savoirfairelinux.com/thruk/cgi-bin/status.cgi?host=$HOSTNAME$\n\n Client : $HOSTNOTES$\n" | /usr/bin/mail -s "** $NOTIFICATIONTYPE$ Service Alert: $HOSTALIAS$/$SERVICEDESC$ is $SERVICESTATE$ **" $CONTACTEMAIL$'
  }
  nagios_command {'notify-host-by-email-once':
    command_line => '/usr/bin/test $HOSTNOTIFICATIONNUMBER$ -le 1 -o $NOTIFICATIONTYPE$ = RECOVERY && /usr/bin/printf "%b" "***** Nagios *****\n\nNotification Type: $NOTIFICATIONTYPE$\nHost: $HOSTNAME$\nState: $HOSTSTATE$\nAddress: $HOSTADDRESS$\nInfo:\n\n$HOSTOUTPUT$ $LONGHOSTOUTPUT$\n\nDate/Time: $LONGDATETIME$\n\nLink : https://monitoring.savoirfairelinux.com/thruk/cgi-bin/status.cgi?host=$HOSTNAME$\n\n Client : $HOSTNOTES$\n" | /usr/bin/mail -s "** $NOTIFICATIONTYPE$ Host Alert: $HOSTNAME$ is $HOSTSTATE$ **" $CONTACTEMAIL$ -a From:$HOSTNAME$@shinken.savoirfairelinux.net'
  }
  nagios_command {'notify-service-by-email-once':
    command_line => '/usr/bin/test $SERVICENOTIFICATIONNUMBER$ -le 1 -o $NOTIFICATIONTYPE$ = RECOVERY && /usr/bin/printf "%b" "***** Nagios *****\n\nNotification Type: $NOTIFICATIONTYPE$\n\nService: $SERVICEDESC$\nHost: $HOSTALIAS$\nAddress: $HOSTADDRESS$\nState: $SERVICESTATE$\n\nDate/Time: $LONGDATETIME$\n\nAdditional Info:\n\n$SERVICEOUTPUT$ $LONGSERVICEOUTPUT$\n\nLink : https://monitoring.savoirfairelinux.com/thruk/cgi-bin/status.cgi?host=$HOSTNAME$\n\n Client : $HOSTNOTES$\n" | /usr/bin/mail -s "** $NOTIFICATIONTYPE$ Service Alert: $HOSTALIAS$/$SERVICEDESC$ is $SERVICESTATE$ **" $CONTACTEMAIL$ -a From:$HOSTNAME$@shinken.savoirfairelinux.net'
  }
}
