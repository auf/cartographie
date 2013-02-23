#
# virtualhost definition
#
define comanche::virtualhost::cgibin(
  $apache2_rootdir      = $comanche::variables::rootdir,
  $vhostname=$name,
  $rules = ["/cgi-bin/:$comanche::variables::wwwrootdir/$vhostname/cgi-bin"]
) {
  if (!defined(Comanche::Module['cgi'])) {
    comanche::module { 'cgi': }
  }

  concat::fragment {"apache2vhost_${name}_cgibin":
    target  => "${apache2_rootdir}/sites-available/${name}.conf",
    content => template('comanche/virtualhostCgibin.conf.erb'),
    order   => 05
  }
}
