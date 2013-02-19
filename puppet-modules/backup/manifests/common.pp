class backup::common {
  if ! defined(File['/usr/local/sysadmin']) {
    file { '/usr/local/sysadmin':
      ensure => 'directory',
      owner  => 'root',
      mode   => '0755',
    }
  }
  file { '/usr/local/sysadmin/validate-rsync.sh':
    ensure  => 'file',
    source  => 'puppet:///modules/backup/validate-rsync.sh',
    owner   => 'root',
    mode    => '0755',
    require => File['/usr/local/sysadmin'],
  }
  file { '/var/backups':
    ensure => 'directory',
    owner  => 'root',
    group  => 'root',
    mode   => '0755',
  }
}
