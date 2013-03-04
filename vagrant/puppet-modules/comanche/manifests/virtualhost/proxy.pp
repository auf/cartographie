#
# virtualhost definition
#
define comanche::virtualhost::proxy(
  $apache2_rootdir      = $comanche::variables::rootdir,
  $rules =[]
) {
  if (!defined(Comanche::Module['proxy'])) {
    comanche::module { 'proxy': }
  }
  if (!defined(Comanche::Module['proxy_http'])) {
    comanche::module { 'proxy_http': }
  }

  concat::fragment {"apache2vhost_${name}_proxy":
    target  => "${apache2_rootdir}/sites-available/${name}.conf",
    content => template('comanche/virtualhostProxy.conf.erb'),
    order   => 20
  }
}
