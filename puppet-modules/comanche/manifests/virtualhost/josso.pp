#
# virtualhost definition
#
define comanche::virtualhost::josso(
  $apache2_rootdir      = $comanche::variables::rootdir,
  $location= '/',
  $authname,
  $gatewayUrl,
  $gatewayendpoint,
  $requiredRoles=[]
) {
  if (!defined(Comanche::Module['authz_default'])) {
    comanche::module { 'authz_default': }
  }
  if (!defined(Comanche::Module['authz_host'])) {
    comanche::module { 'authz_host': }
  }
  if (!defined(Comanche::Module['auth_josso'])) {
    comanche::module { 'auth_josso': }
  }
  if (!defined(File["${apache2_rootdir}/modules/libmod_auth_josso.so"])) {
    file {"${apache2_rootdir}/modules/libmod_auth_josso.so":
      source => "puppet:///modules/comanche/libmod_auth_josso-${architecture}-1.8.6.so",
      mode   => 755
    }
  }


  concat::fragment {"apache2vhost_${name}_josso":
    target  => "${apache2_rootdir}/sites-available/${name}.conf",
    content => template('comanche/virtualhostJosso.conf.erb'),
    order   => 12
  }
}
