class shinken::client (
  $allowed_hosts = '127.0.0.1',
  $critical_queue_size = "150",
  $warning_queue_size = "50",
  $critical_memory = "5",
  $warning_memory = "20",
  $critical_disk = "8",
  $warning_disk = "15",
  $warning_load1  = "15",
  $warning_load5  = "10",
  $warning_load15 = "5",
  $critical_load1  = "30",
  $critical_load5  = "25",
  $critical_load15 = "20",
  $extra_nrpe_commands = [],
  $ignored_disks = [],
  $extra_disk_args = '',
){
  include shinken::params
  if $osfamily == 'RedHat' {
    package { 'nagios-plugins-all':
    ensure => present
    }
    package { 'nagios-plugins-nrpe':
    ensure => present
    }
      if $::architecture == 'x86_64' {
        file { '/usr/lib/nagios':
        ensure => link,
        target => '/usr/lib64/nagios', 
        }
      }
  }


  package { [
    'nagios-plugins',
    'nsca',
    $shinken::params::nrpe_package
    ]:
    ensure => present
  }
  
  user { 'nagios':
    ensure => present,
    #needed for basic puppet yaml file age check
    groups  => ['puppet'],
    require => Package[ $shinken::params::nrpe_package ],
    notify  => Service[ $shinken::params::nrpe_service ],
  }

  file { '/usr/lib/nagios/plugins/':
    ensure  => directory,
    owner   => 'root',
    group   => 'root',
    mode    => 755,
    recurse => true,
    source  => 'puppet:///modules/shinken/plugins',
    require => Package['nagios-plugins'],
  }
  
  file { '/var/run/nagios/':
    ensure  => directory,
    owner   => 'nagios',
    group   => 'root',
    mode    => 755,
    require => Package[ $shinken::params::nrpe_package ],
  }

  #need to ask centOS or redhat to include nrpe_local.cfg in nrpe.cfg
  if $osfamily == 'RedHat' {
    file { '/etc/nagios/nrpe.cfg':
      ensure => present,
      owner   => 'nagios',
      group   => 'nagios',
      mode    => 644,
      source => 'puppet:///modules/shinken/nrpe.cfg-centos',
      require => Package[ $shinken::params::nrpe_package ],
      notify  => Service[ $shinken::params::nrpe_service ],
    }

    #The following template (nrpe_local.cfg.erb) uses vars:
    # critical_memory,warning_memory,
    # critical_load and warning_load values for 1m,5m,15m
    # critical_queue_size, warning_queue_size,
    #It also use lists:
    # extra_nrpe_commands
    # ignored_disks
    # extra_disk_args

    file { '/etc/nagios/nrpe_local.cfg':
      ensure  => present,
      owner   => 'nagios',
      group   => 'nagios',
      mode    => 644,
      content => template('shinken/nrpe_local.cfg.erb'),
      require => Package[ $shinken::params::nrpe_package ],
      notify  => Service[ $shinken::params::nrpe_service ],
    }

    # selinux type for plugins
    if $::selinux_current_mode == 'enforcing' {
      file { '/usr/lib/nagios/plugins/check_mem.pl':
        ensure => file,
        owner   => 'root',
        group   => 'root',
        mode    => 755,
        source => 'puppet:///modules/shinken/plugins/check_mem.pl',
        seltype => 'nagios_system_plugin_exec_t',
      }
      file { '/usr/lib/nagios/plugins/check_disk':
        ensure => file,
        owner   => 'root',
        group   => 'root',
        mode    => 755,
        seltype => 'nagios_unconfined_plugin_exec_t',
      }
    }
  }
  # else Debian-based distro
  else {
    file { '/etc/nagios/nrpe_local.cfg': 
      ensure  => present,
      owner   => 'nagios',
      group   => 'nagios',
      mode    => 640,
      content => template('shinken/nrpe_local.cfg.erb'),
      require => Package[ $shinken::params::nrpe_package ],
      notify  => Service[ $shinken::params::nrpe_service ],
    }
    file { '/etc/nagios/nrpe.cfg':
      ensure => present,
      owner   => 'nagios',
      group   => 'nagios',
      mode    => 644,
      source => 'puppet:///modules/shinken/nrpe.cfg-debian',
      require => Package[ $shinken::params::nrpe_package ],
      notify  => Service[ $shinken::params::nrpe_service ],
    }
  }

  service { $shinken::params::nrpe_service:
    ensure     => running,
    enable     => true,
    require    => Package[ $shinken::params::nrpe_package ],
    hasstatus  => $shinken::params::nrpe_has_status,
    hasrestart => true,
    #trying to use only the pattern https://groups.google.com/group/puppet-users/browse_thread/thread/299b3c9373419f0c?pli=1
    pattern    => 'nrpe',
    #restart    => "/etc/init.d/${shinken::params::nrpe_service} reload",
    #status     => "/etc/init.d/${shinken::params::nrpe_service} status", 
    #subscribe  => File['/etc/nagios/nrpe_local.cfg'], #just in case, monitor changes actively
  }

  service { 'nsca':
    ensure      => stopped,
    enable      => false,
    hasstatus   => false,
    pattern     => '/usr/sbin/nsca',
    hasrestart  => true,
    require     => Package['nsca']
  }
}
