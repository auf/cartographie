set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab
set wildmenu
set showcmd

syntax on

filetype plugin indent on

if &term == "builtin_gui"
    set t_Co=256
    colorscheme sienna
elseif &term == "linux"
    set t_Co=8
elseif &term == "screen"
    set t_Co=16
elseif &term == "xterm"
    set t_Co=256
elseif &term =~ "^rxvt-unicode$"
    set t_Co=88
endif	
colorscheme elflord

map ,p :r!pwgen -n -c<CR>
map ,v :set invpaste paste?<CR>
set pastetoggle=,v
set paste
