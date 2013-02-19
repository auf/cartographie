##   = Class: apt::server
##  
##   * Install and configure a repository for debian packages in $path 
##   * _INFO_: Currently only ubuntu is supported/tested
##  
##   == Parameters
##  
##   $distversions [] :: The distversion (hardy, lucid...) this repository is supporting
##   $reponame :: A name to identify the repository (ex: the client name)
##   $repopath :: The path to the local repository folder
##   $owner :: The owner of the directories
##   $group :: The group of the directories

define apt::server (
  $repobase = "/var/www/repository",
  $reponame = $name,
  $distversions = ['lucid'],
  $owner = "root",
  $group = "root"
  ) {
  $repopath = "${repobase}/${reponame}"
  exec { "mkdirp_${repopath}":
    unless => "/usr/bin/test -d ${repopath}",
    command => "/bin/mkdir -p ${repopath}",
  }
  file { "${repopath}":
    ensure => directory,
    require => Exec["mkdirp_${repopath}"],
    owner  => $owner,
    group  => $group,
    mode  => 0755,
  }
  file { [
          "${repopath}/conf",
          "${repopath}/db",
          "${repopath}/dists",
          "${repopath}/incoming",
          "${repopath}/pool",
         ]:
    ensure => directory,
    owner  => $owner,
    group  => $group,
    mode  => 0755,
  }
  file { "${repopath}/conf/distributions":
    ensure   => present,
    content  => template("apt/distributions.erb"),
    owner    => $owner,
    group    => $group,
    mode     => 0644,
  }

}
