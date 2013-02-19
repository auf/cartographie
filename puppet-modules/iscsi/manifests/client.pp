
# http://www.howtoforge.com/using-iscsi-on-debian-lenny-initiator-and-target
class iscsi::client {
  package { 'open-iscsi':
    ensure => present,
  }
    
  service {'open-iscsi':
    ensure        => running,
    enable        => true,
    hasstatus     => true,
    hasrestart    => true,
    require => Package['open-iscsi']
  }

  file { '/etc/iscsi':
    ensure => directory,
    require => Package['open-iscsi'],
  }
    
  file { '/etc/iscsi/nodes':
    ensure => directory,
    require => File["/etc/iscsi"],
  }
    
  # specify that node.startup = automatic
  file { '/etc/iscsi/iscsid.conf':
    source=> 'puppet:///iscsi/iscsid_client.conf',
    require => Package['open-iscsi'],
    notify => Service['open-iscsi']
  }
    
  Iscsi::Client::LoginVolume <<| tag == "iscsi-${environment}" |>>
    
  # we should now find volume in /dev/disk/by-path/ip-${iscsi_ipaddress}:3260-iscsi-iqn.2001-04.com.puppet:sto.${iscsi_volumegroup}.${iscsi_volumename}-lun-0

  # note for debug:
  #
  # iscsiadm -m node -T iqn.2001-04.com.company:storage.lun0 -p 192.168.50.217 --login (ou logout)
  # iscsiadm -m discovery -t st -p 192.168.50.217
  # iscsiadm -m node -T iqn.2006-01.com.openfiler:scsi.linux3-data-1 -p 192.168.2.195 --op update -n node.startup -v automatic
  # iscsiadm -m node --targetname "iqn.2001-04.com.example:storage.lun1" --portal "192.168.0.101:3260" --login OU on redemarre le service
  # /dev/disk/by-path/ip-192.168.50.217:3260-iscsi-iqn.2001-04.com.puppet:storage.vg0.storage_lun0-lun-0
}



#
# function used to export configuration to iscsi client.
# $iscsi_iqn should looks like iqn.2001-04.com.puppet:sto.vg0.myvolume
define iscsi::client::loginVolume ($iscsi_user,$iscsi_password, $iscsi_iqn, $iscsi_ipaddress) {
  file { "/etc/iscsi/nodes/${iscsi_iqn}/":
    ensure => directory,
  }
  file { "/etc/iscsi/nodes/${iscsi_iqn}/${iscsi_ipaddress},3260,1":
    ensure => directory,
    require => File["/etc/iscsi/nodes/${iscsi_iqn}/"],
  }

  file { "/etc/iscsi/nodes/${iscsi_iqn}/${iscsi_ipaddress},3260,1/default":
    require => File["/etc/iscsi/nodes/${iscsi_iqn}/${iscsi_ipaddress},3260,1"],
    content => template('iscsi/iscsiVolume.erb'),
  }
    
  exec { 'iscsi_client_loginVolume':
    command   => "/sbin/iscsiadm -m node -T ${iscsi_iqn} -p $iscsi_ipaddress --logout; /sbin/iscsiadm -m node -T ${iscsi_iqn} -p $iscsi_ipaddress --login",
    subscribe       => File["/etc/iscsi/nodes/${iscsi_iqn}/${iscsi_ipaddress},3260,1/default"],
#   refreshonly     => true,
    require         => File["/etc/iscsi/nodes/${iscsi_iqn}/${iscsi_ipaddress},3260,1/default"]
  }
}

