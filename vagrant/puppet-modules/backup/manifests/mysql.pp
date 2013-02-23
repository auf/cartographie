# class: backup::mysql
#    creates mysqldump files in /var/backups
class backup::mysql (
  $delay_compress = false,
  $bzip2 = false,
  $hour = 3,
  $minute = 5
){
    require backup::common

    # simple class to produce daily backups of mysql databases in a folder,
    # every day, kept for a week.
    # should eventually control: backup destination, .cnf source and mysql folder location.
    # be careful, run-parts looks for a specific naming convention...
    file { '/usr/local/sysadmin/backupmysql':
      ensure  => file,
      content => template('backup/backupmysql.erb'),
      owner   => 'root',
      group   => 'root',
      mode    => '0755',
    }
    file { '/etc/cron.d/backupmysql':
      ensure  => present,
      content => "${minute} ${hour} * * * root /usr/local/sysadmin/backupmysql\n",
      owner   => 'root',
      group   => 'root',
      mode    => '0644',
    }
    file { '/etc/cron.daily/backupmysql':
      ensure  => absent,
    }
    file { '/var/backups/mysql':
      ensure => directory,
      owner  => 'root',
      group  => 'root',
      mode   => '0750',
    }
}
