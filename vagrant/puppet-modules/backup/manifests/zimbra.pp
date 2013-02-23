class backup::zimbra {
  ### DESCRIPTION ###
  # Adds the necessary sysadmin scripts to create an LVM snapshot of the
  # /opt folder and remove it, so that it can be used with rsnapshot
  # or bacula.
  # In order: createSnapshotZimbra.sh stops zimbra, create snapshot, starts zimbra,
  #  mounts snapshot into /mnt/optsnapshot.
  #            (then you do your backup on /mnt/optsnapshot/zimbra)
  # Then, delete snapshot with deleteSnapshotZimbra.sh

  # example of usage in rsnapshot.conf:
  # cmd_preexec     /usr/local/sysadmin/createSnapshotZimbra.sh
  # cmd_postexec    /usr/local/sysadmin/deleteSnapshotZimbra.sh

  # example of usage in bacula job def:
  #   ClientRunBeforeJob      = "/usr/local/sysadmin/createSnapshotZimbra.sh"
  #   ClientRunAfterJob       = "/usr/local/sysadmin/deleteSnapshotZimbra.sh"


  ### VARIABLES ###
  # requires: $volgroupName

  require backup::common
  file { "/usr/local/sysadmin/createSnapshotZimbra.sh":
    ensure => "file",
    content => template("backup/createSnapshotZimbra.sh.erb"),
    owner => root,
    mode => 755;
  }
  file { "/usr/local/sysadmin/deleteSnapshotZimbra.sh":
    ensure => "file",
    content => template("backup/deleteSnapshotZimbra.sh.erb"),
    owner => root,
    mode => 755;
  }
}
