#
# virtualhost definition
#
define comanche::virtualhost::alias(
  $apache2_rootdir      = $comanche::variables::rootdir,
  $rules      = []
) {
  if (!defined(Comanche::Module['alias'])) {
    comanche::module { 'alias': }
  }
  concat::fragment {"apache2vhost_${name}_alias":
    target  => "${apache2_rootdir}/sites-available/${name}.conf",
    content => template('comanche/virtualhostAlias.conf.erb'),
    order   => 15
  }
}
