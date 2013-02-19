
#
class iscsi::server {
  
  package { 'iscsitarget':
    ensure => present,
  }
     
  service {'iscsitarget':
    ensure                => running,
    enable                => true,
    hasstatus             => true,
    hasrestart    => true,
    require => Package['iscsitarget'],
  }

    # specify that iscsi is enabled
  file { '/etc/default/iscsitarget':
    content => "ISCSITARGET_ENABLE=true\n",
    require => Package['iscsitarget'],
    notify => Service['iscsitarget'],
  }
    
  # specify that the system must be launch at boot
  file { '/etc/iscsi':
    ensure => directory,
    require => Package['iscsitarget'],
  }
  file { '/etc/iscsi/iscsid.conf':
    source => 'puppet:///iscsi/iscsid_server.conf',
    require => File['/etc/iscsi'],
    notify => Service['iscsitarget']
  }
    
  # list LVM volume exported
  include concat::setup 
  concat { '/etc/ietd.conf':
    require => Package['iscsitarget'],
  }
  concat::fragment { 'iscsi_ietd.conf_begin':
    target => '/etc/ietd.conf',
    content => template('iscsi/ietd.conf.erb'),
    order => 01,
  }
}    
    


define iscsi::server::exportLvmVolume( $iscsi_user,$iscsi_password, $iscsi_volumegroup, $iscsi_volumename, $iscsi_ipaddress = $ipaddress, $iscsi_exportviapuppet=true) {
  concat::fragment { "iscsi_ietd.conf_${iscsi_volumegroup}_${iscsi_volumename}":
    order => 50,
    target => '/etc/ietd.conf',
    content  => template('iscsi/ietd.conf_part.erb'),
    notify => Service['iscsitarget'],
  }
        
  if ($iscsi_exportviapuppet==true) {
    # we export client configuration
    @@iscsi::client::loginVolume { "iscsi_exportVolume_${iscsi_volumegroup}_${iscsi_volumename}_${iscsi_ipaddress}": 
      iscsi_user => $iscsi_user,
      iscsi_password => $iscsi_password,
      iscsi_iqn => "iqn.2001-04.com.puppet:sto.${iscsi_volumegroup}.${iscsi_volumename}",
      iscsi_ipaddress => $iscsi_ipaddress,
      tag => "iscsi-${environment}",
    }
  }
}



