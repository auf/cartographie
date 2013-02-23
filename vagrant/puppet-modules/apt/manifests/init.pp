import "server/*.pp"

# = Class: apt
#
# * Provide aptitude-update exec
# * Setup cron to update apt every 4h, at 10th minute
# * Set proper right on sources.list
# * Allow use of unauthenticated packages (This might change when keyserver will function properly)
# * Fill sources.list content
#
# === Parameters:
#
# $my_region:: The region we are in. This will result in automatic selection of geographical best source for downloads
# $apt_local_mirror:: The url to the local mirror that might be setup. This OVERRIDES the $my_region value.
class apt (
  $stage                = pre,
  $apt_forceYes         = true,
  $apt_enable_proposed  = false,
  $aptGetSrc            = false,
  $apt_local_mirror     = false,
  $my_region            = 'ca'
  ) {
  
  include apt::variables
  $apt_dir          = $apt::variables::apt_dir
  $apt_sources_dir  = $apt::variables::apt_sources_dir
  $apt_conf_dir     = $apt::variables::apt_conf_dir
  $apt_section      = $apt::variables::apt_section
  
  #Provides add-apt-repository command
  package { 'python-software-properties':
    ensure  => present
  }

  exec { 'aptitude-update':
    command     => 'aptitude update',
    refreshonly => true,
  }

  file {
    'sources.list.d':
      path      => $apt_sources_dir,
      ensure    => directory,
      checksum  => md5,
      mode      => 0755,
  }

  file {
    'sources.list.d/puppet':
      path      => "${apt_sources_dir}/puppet",
      ensure    => directory,
      checksum  => md5,
      mode      => 0755,
      purge     => true,
      recurse   => true,
      force     => true,
      ignore    => [ 'README', "manual_*"],
      require   => File [ 'sources.list.d' ]
  }

  #This was done because of keyservers problems
  file {
    '80forceyes':
      path     => "${apt_conf_dir}/80forceyes",
      ensure   => file,
      checksum => md5,
      owner    => root,
      group    => root,
      mode     => 0644,
      content  => template('apt/conf/80forceyes.erb'),
  }



  if $apt_local_mirror {
    $apt_url = $apt_local_mirror
  } else {
    if $ec2_instance_id != '' {
      $apt_url = "http://${ec2_placement_availability_zone}.archive.ubuntu.com/ubuntu/"
    } else {
      case $::lsbdistid {
        Debian:	{	$apt_url = $my_region ? {
          'ca'    => 'http://debian.savoirfairelinux.net/debian',
          default => 'http://ftp.fr.debian.org/debian/',
          }
        }
        Ubuntu: {	$apt_url = $my_region ? {
          'ca'    => 'http://ubuntu.mirror.iweb.ca/',
          default	=> 'http://eu.archive.ubuntu.com/ubuntu/',
          }
        }
      }
    }
  }

  #The require here only ensures that the package installation does not happen between when sources.list is changed
  #and between when aptitude-update is refreshed
  file { 'sources.list':
    path      => "${apt_dir}/sources.list",
    ensure    => file,
    mode      => 0644,
    content   => template('apt/sources.list.erb'),
    notify    => Exec ['aptitude-update'],
    require   => Package['python-software-properties'],
  }
}
