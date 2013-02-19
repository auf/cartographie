class shinken::client::megaraid::requirements {
  #note: you will need an additionnal repository like hwraid.le-vert....
  include apt::repository::hwraid
  package { "megactl": 
    ensure  => present, 
  }
}
