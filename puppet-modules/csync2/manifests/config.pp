class csync2::config (
  $csync2_group,
  $csync2_include,
  $csync2_masterhosts,
  $csync2_slavehosts,
  $csync2_exclude = [],
  $csync2_backup_directory = '/var/backups/csync2', 
  $csync2_backup_generation = 3,
  $csync2_auto
  ) {
  
  if ! $csync2_group { fail("csync2_group not defined!") }
  if ! $csync2_masterhosts { fail("csync2_masterhosts not defined!") }
  if ! $csync2_slavehosts { fail("csync2_slavehosts not defined!") }
  if ! $csync2_include { fail("csync2_include not defined!") }
  if ! $csync2_exclude { $csync2_exclude=[] }
  if ! ($csync2_auto in ['first', 'younger', 'older', 'bigger', 'smaller', 'none']) {
    fail("csync2_auto defined with an unknown value!")
  } 

  if $csync2_backup_directory != false {
    file { $csync2_backup_directory:
      ensure => directory,
      mode   => '0750',
      owner  => 'root',
      group  => 'root',
    }
  }
  include concat::setup
  concat { "/etc/csync2.cfg" :
    require => [ Class['csync2::install'], Class['csync2::key'] ],
  }
  concat::fragment{ "csync2simplecfg_start" :
    target  => '/etc/csync2.cfg',
    order   => 1,
    content => "# This file is managed by puppet, do not edit manually\ngroup $csync2_group {\n"
  }
  
  #simplecfg_end contains pretty much everything except actions
  concat::fragment{ "csync2simplecfg_end":
    target  => '/etc/csync2.cfg',
    order   => 99,
    content => template("csync2/simplecfg_end.erb")
  }
}
