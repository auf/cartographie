account {'dummy':
  email       => 'dummy.boy@gmail.com',
  fullname    => 'Dummy Boy',
  shell       => '/bin/bash',
  vim         => true,
  bash        => true,
  git         => true,
  ssh_key     => 'AAAAB3NzaC1yc2EAAAADAQABAAABAQDJxu0pfj/dsiqrvcYqiVjQk/e9JoyaYUL8WOzjPG9ssXJ97H1sdks8n+btXblgDWBEzyhYtWv0v5zYgDtqp3Bc5k7rL9O+W6bvsn05aTV48OQHysW5NUv/NwTNICff79M5Wyl+S7158J0YaX',
  ssh_keytype => 'ssh-rsa',
  ssh_name    => 'dummy@localhost',
  ensure      => absent,
  rmhome      => true,
}

account {'bunny':
  email       => 'bunny.boy@gmail.com',
  fullname    => 'Bunny Boy',
  shell       => '/bin/bash',
  vim         => true,
  bash        => true,
  git         => true,
  ssh_key     => 'AAAAB3NzaC1yc2EAAAADAQABAAABAQDJxu0pfj/dsiqrvcYqiVjQk/e9JoyaYUL8WOzjPG9ssXJ97H1sdks8n+btXblgDWBEzyhYtWv0v5zYgDtqp3Bc5k7rL9O+W6bvsn05aTV48OQHysW5NUv/NwTNICff79M5Wyl+S7158J0YaX',
  ssh_keytype => 'ssh-rsa',
  ssh_name    => 'bunny@localhost',
  ensure      => absent,
  rmhome      => true,
}
