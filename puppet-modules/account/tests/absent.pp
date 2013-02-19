account {'dummy':
  ensure   => 'absent',
  email    => 'dummy.boy@gmail.com',
  fullname => 'Dummy Boy',
  shell    => '/bin/bash',
}
