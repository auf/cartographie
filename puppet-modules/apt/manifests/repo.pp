# = Define: repo
#
# === Parameters:
#
# $repo:: The repository name. Puppet will search for $repo.list.erb in its templates
# $source (None):: If provided, puppet will get content from $source.list in its files
# $ensure (enabled):: Whether we want to add or remove this repository
# $url (None):: url where to find the root repository. In the deb http://ubuntu.mirror.iweb.ca/ lucid main restricted universe multiverse, this is the second parameter
# $append_lsbdistcodename (true):: if the distribution must figure. In the deb http://ubuntu.mirror.iweb.ca/ lucid main restricted universe multiverse it is the third parameter
# $section (default depending on distrition):: to override the section listed. In the deb http://ubuntu.mirror.iweb.ca/ lucid main restricted universe multiverse, this is the remaining (main restricted universe multiverse) parameters
# === Example
# To load hudson package (http://pkg.hudson-labs.org/debian/) and put "deb http://pkg.hudson-labs.org/debian binary/":
#
#   apt::repo { "hudson": url => "http://pkg.hudson-labs.org/debian", append_lsbdistcodename => false, section => 'binary/' }
#
#
define apt::repo(
  $ensure                 = enabled,
  $source                 = 'None',
  $url                    = 'None',
  $repo_suffix            = false,
  $append_lsbdistcodename = true,
  $forced_lsbdistcodename = $::lsbdistcodename,
  $section                = $apt::variables::apt_section,
  $aptGetSrc              = false,
  $keyid                  = false
  ) {
  
  include apt::variables
  $apt_dir          = $apt::variables::apt_dir
  $apt_sources_dir  = $apt::variables::apt_sources_dir
  $apt_conf_dir     = $apt::variables::apt_conf_dir
  $apt_section      = $apt::variables::apt_section
  
  file { "${apt_sources_dir}/puppet/${name}.list":
    ensure  => $ensure ? {
      enabled  => file,
      disabled => absent,
    },
    mode     => 0644,
    content  => $source ? {
      'None'  => template('apt/standardRepo.list.erb'),
      default => undef
    },
    source => $content ? {
      'None'  => "puppet:///modules/apt/${source}",
      default => undef
    },
    notify   => Exec['aptitude-update'],
  }

  file { "${apt_sources_dir}/${name}.list" :
      ensure  => $ensure ? {
        enabled  => link,
        disabled => absent,
      },
      target  => "${apt_sources_dir}/puppet/${name}.list",
      notify  => Exec['aptitude-update']
  }
  
  if $keyid {
    #Only found workaround to be able to have the same keyid for different repositories
    if ! defined(Exec["Import $keyid to apt keystore"]) {
      apt::key { $name:
        keyid  => $keyid,
        ensure => present
      }
    }
    realize Apt::Key[$name]
  }
}