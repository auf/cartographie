class shinken::config::commands {

  @@nagios_command { 'check_nagios':
    command_line  => '$USER1$/check_nagios -e 5 -F /var/log/nagios3/nagios.log -C /usr/sbin/nagios3'
  }

  @@nagios_command { 'check_mysql_replication':
    command_line   => '$USER1$/check_mysql_replication.sh -H $ARG1$'
  }

  @@nagios_command { 'check_dummy':
    command_line    => '$USER1$/check_dummy $ARG1$ $ARG2$'
  }
  @@nagios_command { 'check_nrpe':
    command_line   =>       '_nrpe_poller -H $HOSTADDRESS$ -t 60 -c $ARG1$'
  }
  @@nagios_command { 'check_nrpe_slow':
    command_line   =>       '_nrpe_poller -H $HOSTADDRESS$ -t 600 -c $ARG1$'
  }
  @@nagios_command { 'check_nrpe_with_relay':
    command_line   =>       '_nrpe_poller -H $ARG1$ -t 60 -c $ARG2$'
  }
  ### Base Checks ###

  @@nagios_command { 'check_ping':
     command_line   =>       '$USER1$/check_ping -H $HOSTADDRESS$ -w 2000,20% -p 6 -c 5000,50%'
  }

  @@nagios_command { 'check_ping_specific':
     command_line   =>       '$USER1$/check_ping -H $ARG1$ -w 2000,20% -p 6 -c 5000,50%'
  }

  @@nagios_command { 'check_shinken_arbiter':
     command_line   =>       '$USER1$/check_shinken.py -t arbiter -a $HOSTADDRESS$'
  }

  @@nagios_command { 'check_ldap':
     command_line   =>       '$USER1$/check_ldap -3 -H $HOSTADDRESS$ -w $ARG1$ -c $ARG2$ -b $ARG3$'
  }

  @@nagios_command { 'check_ldaps':
    command_line => '$USER1$/check_ldap -3 -H $ARG4$ -w $ARG1$ -c $ARG2$ -b $ARG3$ --ssl'
  }

  @@nagios_command { 'check_ldap_tls':
     command_line => '$USER1$/check_ldap -3 -H $ARG4$ -w $ARG1$ -c $ARG2$ -b $ARG3$ --starttls'
  }


  @@nagios_command { 'check_shinken_scheduler':
     command_line   =>       '$USER1$/check_shinken.py -t scheduler -a $HOSTADDRESS$'
  }

  @@nagios_command { 'check_shinken_reactionner':
     command_line   =>       '$USER1$/check_shinken.py -t reactionner -a $HOSTADDRESS$'
  }

  @@nagios_command { 'check_shinken_poller':
     command_line   =>       '$USER1$/check_shinken.py -t poller -a $HOSTADDRESS$'
  }

  @@nagios_command { 'check_shinken_broker':
     command_line   =>       '$USER1$/check_shinken.py -t broker -a $HOSTADDRESS$'
  }

  @@nagios_command { 'check_host_alive':
     command_line   =>       '$USER1$/check_ping -H $HOSTADDRESS$ -w 5000,100% -c 5000,100% -p 1'
  }

  @@nagios_command { 'check_disk':
     command_line   =>       '$USER1$/check_disk -w $ARG1$ -c $ARG2$ -e'
  }

  @@nagios_command { 'check_ftp':
     command_line   =>       '$USER1$/check_ftp -H $HOSTADDRESS$ -t 42 -w $ARG1$ -c $ARG2$'
  }

  @@nagios_command { 'check_load':
     command_line   =>       '$USER1$/check_load -w $ARG1$ -c $ARG2$'
  }

  @@nagios_command { 'check_cpu':
     command_line    =>      '$USER1$/check_cpu.sh -w $ARG1$ -c $ARG2$'
  }

  @@nagios_command { 'check_tcp':
     command_line    =>      '$USER1$/check_tcp -H $ARG1$ -p $ARG2$'
  }

  @@nagios_command { 'check_ssh':
     command_line    =>      '$USER1$/check_ssh -p $ARG1$ -H $HOSTADDRESS$'
  }
  ### Memcached ###
  @@nagios_command { 'check_memcached_connectiontime':
     command_line   =>       '$USER1$/check_memcached.py -H $HOSTADDRESS$ -t $ARG1$ -p $ARG2$ '
  }

  @@nagios_command { 'check_memcached_hitrate':
     command_line   =>       '$USER1$/check_memcached -v hitrate -H $HOSTADDRESS$ -w $ARG1$ -c $ARG2$'
  }

  @@nagios_command { 'check_memcached_getrate':
     command_line   =>       '$USER1$/check_memcached -v getrate -H $HOSTADDRESS$ -w $ARG1$ -c $ARG2$'
  }

  ### Web services ###

  @@nagios_command { 'check_tcp_80':
     command_line   =>       '$USER1$/check_tcp -H $HOSTADDRESS$ -p 80'
  }

  @@nagios_command { 'check_tcp_443':
     command_line   =>       '$USER1$/check_tcp -H $HOSTADDRESS$ -p 443'
  }

  @@nagios_command { 'check_http':
     command_line   =>       '$USER1$/check_http -t 42 -H $ARG1$'
  }

  @@nagios_command { 'check_https':
     command_line   =>       '$USER1$/check_http -t 42 --ssl -H $ARG1$'
  }

  @@nagios_command { 'check_https_with_auth':
     command_line   =>       '$USER1$/check_http -t 42 --ssl -H $ARG1$ -e 401'
  }

  @@nagios_command { 'check_http_with_auth':
     command_line   =>       '$USER1$/check_http -t 42 -H $ARG1$ --ssl -e 401'
  }
  
  @@nagios_command { 'check_http_with_auth_nossl':
     command_line   =>       '$USER1$/check_http -t 42 -H $ARG1$ --authorization=leonardi:recconectsyou'
  }

  @@nagios_command { 'check_apache2':
     command_line   =>       '$USER1$/check_apache2.sh'
  }

  @@nagios_command { 'check_website':
     command_line   =>       '$USER1$/check_http -t 42 -w $ARG1$ -c $ARG2$ -H $ARG3$ -u $ARG4$ -p $ARG5$'
  }

  @@nagios_command { 'check_website_with_expect_string':
     command_line   =>       '$USER1$/check_http -t 42 -w $ARG1$ -c $ARG2$ -H $ARG3$ -u $ARG4$ -p $ARG5$ -s $ARG6'
  }

  @@nagios_command { 'check_website_ssl':
     command_line   =>       '$USER1$/check_http -t 42 -S -w $ARG1$ -c $ARG2$ -H $ARG3$ -u $ARG4$ -p $ARG5$'
  }

  @@nagios_command { 'check_website_ssl_with_expect_string':
     command_line   =>       '$USER1$/check_http -t 42 -S -w $ARG1$ -c $ARG2$ -H $ARG3$ -u $ARG4$ -p $ARG5$ -s $ARG6'
  }

  @@nagios_command { 'check_certificate':
     command_line   =>       '$USER1$/check_http -H $HOSTADDRESS$ -C $ARG1$'
  }

  ### MySQL ###
  @@nagios_command { 'check_mysql_connectiontime':
     command_line   =>       '$USER1$/check_mysql_health -H $HOSTADDRESS$ --warning $ARG1$ --critical $ARG2$ --username $ARG3$ --password $ARG4$ --mode connection-time'
  }

  @@nagios_command { 'check_mysql_slaveio':
     command_line   =>       '$USER1$/check_mysql_health -H $HOSTADDRESS$ --username $ARG1$ --password $ARG2$ --mode slave-io-running'
  }

  @@nagios_command { 'check_mysql_slavesql':
     command_line   =>       '$USER1$/check_mysql_health -H $HOSTADDRESS$ --username $ARG1$ --password $ARG2$ --mode slave-sql-running'
  }

  @@nagios_command { 'check_tcp_3306':
     command_line   =>       '$USER1$/check_tcp -H $HOSTADDRESS$ -p 3306'
  }

  ### DNS ###
  @@nagios_command { 'check_dns':
     command_line   =>       '$USER1$/check_dns -s $HOSTADDRESS$ -H $ARG1$'
  }
  ### Mail ###
  @@nagios_command { 'check_smtp':
     command_line   =>       '$USER1$/check_smtp -H $HOSTADDRESS$'
  }
  @@nagios_command { 'check_imap':
     command_line   =>       '$USER1$/check_imap -H $HOSTADDRESS$'
  }
  @@nagios_command { 'check_pop':
     command_line   =>       '$USER1$/check_pop -H $HOSTADDRESS$'
  }

  ### Imprimantes ###
  @@nagios_command { 'check_printer_consumables':
     command_line   =>       '$USER1$/check_snmp_printer.sh -H $HOSTADDRESS$ -C $ARG1$ -V $ARG2$ -x "CONSUM ALL"'
  }

  @@nagios_command { 'check_printer_message':
     command_line   =>       '$USER1$/check_snmp_printer.sh -H $HOSTADDRESS$ -C $ARG1$ -V $ARG2$ -x "MESSAGES"'
  }

  ### Windows ###
  @@nagios_command { 'check_nt':
     command_line   =>       '$USER1$/check_nt -H $HOSTADDRESS$ -s zmFqq5tFRlKh -v $ARG1$ $ARG2$'
  }

  ### Libvirt stat###
  @@nagios_command { 'check_libvirt_stats':
     command_line   =>       '$USER1$/check_libvirt_stats.py -u $ARG1$ -U $ARG2$ -w $ARG3$ -c $ARG4$'
  }

  ### Bandwidth stat ###
  @@nagios_command { 'check_bandwidth':
     command_line   =>       '$USER1$/check_bandwidth_usage.py -H $ARG1$ -l $ARG2$ -w $ARG3$ -c $ARG4$ -n $ARG5$ -g -s $ARG6$ -f -d $ARG7$'
  }

  ### ssmtp exim : integration l3i ###
  @@nagios_command { 'check_ssmtp_exim':
     command_line   =>       '$USER1$/check_ssmtp -H $HOSTADDRESS$ --expect=220'
  }

}
