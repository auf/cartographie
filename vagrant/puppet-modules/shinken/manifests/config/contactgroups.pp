class shinken::config::contactgroups {
  @@nagios_contactgroup { 'administrators':
    alias => 'Nagios Administrators'
  }
  
  @@nagios_contactgroup { 'administratorspaget':
    alias => 'Nagios Administrators contacted repeatdly off hours'
  }

  @@nagios_contactgroup { 'administratorsemail':
    alias => 'Nagios Administrators contacted only once, 24/7'
  }
}
