class shinken::config::timeperiods {
  @@nagios_timeperiod { '24x7':
    friday          => '00:00-24:00',
    wednesday       => '00:00-24:00',
    tuesday         => '00:00-24:00',
    sunday          => '00:00-24:00',
    monday          => '00:00-24:00',
    saturday        => '00:00-24:00',
    thursday        => '00:00-24:00',
    alias           => '24 Hours A Day, 7 Days A Week'
  }

  @@nagios_timeperiod { 'WorkHours':
    friday          => '09:00-17:00',
    wednesday       => '09:00-17:00',
    tuesday         => '09:00-17:00',
    monday          => '09:00-17:00',
    thursday        => '09:00-17:00',
    alias           => 'Standard Work Hours'
  }

  @@nagios_timeperiod { 'NonWorkHours':
    friday          => '00:00-09:00,17:00-24:00',
    wednesday       => '00:00-09:00,17:00-24:00',
    tuesday         => '00:00-09:00,17:00-24:00',
    sunday          => '00:00-24:00',
    monday          => '00:00-09:00,17:00-24:00',
    saturday        => '00:00-24:00',
    thursday        => '00:00-09:00,17:00-24:00',
    alias           => 'Non-Work Hours'
  }

  @@nagios_timeperiod { 'CoffeeHours':
    friday          => '07:00-16:00',
    wednesday       => '07:00-16:00',
    tuesday         => '07:00-16:00',
    monday          => '07:00-16:00',
    thursday        => '07:00-16:00',
    alias           => 'Coffee Hours'
  }

  @@nagios_timeperiod { 'CoffeeRavitaillementHours':
    friday          => '00:00-09:00,17:00-24:00',
    wednesday       => '00:00-09:00,17:00-24:00',
    tuesday         => '00:00-09:00,17:00-24:00',
    sunday          => '00:00-24:00',
    monday          => '00:00-09:00,17:00-24:00',
    saturday        => '00:00-24:00',
    thursday        => '00:00-09:00,17:00-24:00',
    alias           => 'Coffee Hours - Ravitaillement'
  }

  @@nagios_timeperiod { 'Never':
     alias           => 'Never'
  }
}
