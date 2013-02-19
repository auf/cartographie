#
# virtualhost definition
#
define comanche::virtualhost::rewrite(
  $apache2_rootdir      = $comanche::variables::rootdir,
  $rules       = []
) {
  if (!defined(Comanche::Module['rewrite'])) {
    comanche::module { 'rewrite': }
  }

  concat::fragment {"apache2vhost_${name}_rewrite":
    target  => "${apache2_rootdir}/sites-available/${name}.conf",
    content => template('comanche/virtualhostRewrite.conf.erb'),
    order   => 15
  }
}
