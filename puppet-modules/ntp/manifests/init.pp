
# = Class: ntp
#
# * Setup proper time management
class ntp (
  $my_region ='europe'
) {
  if $ec2_instance_id == '' { #This is specific to amazon ec2
    case "${lsbdistid}" {
      /(Ubuntu|ubuntu|Debian|debian)/ : {
        class { 'ntp::openntpd':
          my_region => $my_region
        }
      }
      /(centos|RedHatEnterpriseServer)/ : {
        class { 'ntp::standard':
          my_region => $my_region
        }
      }
    }
  } else {
    file { '/etc/localtime':
      ensure  => link,
      target  => $ec2_placement_availability_zone ? {
        /us-east-1/     => "/usr/share/zoneinfo/EST5EDT",
        /us-west-1/     => "/usr/share/zoneinfo/PST8PDT",
        /eu-west-1/     => "/usr/share/zoneinfo/Europe/Dublin",
        /ap-southeast-1/  => "/usr/share/zoneinfo/Singapore",
      },
    }

    file { '/etc/timezone':
      ensure  => file,
      mode  => 0644,
      content => $ec2_placement_availability_zone ? {
        /us-east-1/     => "EST5EDT",
        /us-west-1/     => "PST8PDT",
        /eu-west-1/     => "Dublin",
        /ap-southeast-1/  => "Singapore",
      },
    }

  }
}

