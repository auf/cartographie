account {'dummy':
  email       => 'dummy.boy@gmail.com',
  fullname    => 'Dummy Boy',
  shell       => '/bin/bash',
  ssh_key_ensure => 'absent',
  ssh_key     => 'AAAAB3NzaC1yc2EAAAADAQABAAABAQDJxu0pfj/dsiqrvcYqiVjQk/e9JoyaYUL8WOzjPG9ssXJ97H1sdks8n+btXblgDWBEzyhYtWv0v5zYgDtqp3Bc5k7rL9O+W6bvsn05aTV48OQHysW5NUv/NwTNICff79M5Wyl+S7158J0YaX',
  ssh_keytype => 'ssh-rsa',
  ssh_name    => 'dummy@localhost',
}
