class libvirt {
  package { [
    'qemu-kvm',
    'libvirt',
    ]:
    ensure => installed,
  }
  service { 'libvirtd':
    ensure          => running,
    enable          => true,
    hasstatus       => true,
    require         => Package['libvirt'],
  }
  file { '/etc/libvirt/libvirtd.conf':
    source => 'puppet:///modules/libvirt/libvirtd.conf',
    notify => Service['libvirtd']
  }
  group{'libvirtd':
    ensure => present,
  }
  file { '/etc/profile.d/libvirt.sh':
    ensure  => present,
    content => 'LIBVIRT_DEFAULT_URI=qemu:///system\n',
  }
}
