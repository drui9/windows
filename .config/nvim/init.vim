syntax enable

set wrap!
set number
set secure
set mouse=
set shada=
set viminfo=
set expandtab
set tabstop=4
set cursorline
set autoindent
set noswapfile
set writebackup!
set scrolloff=12
set foldcolumn=2
set shiftwidth=4
set softtabstop=4
set encoding=utf-8
set fileformat=unix
set foldmarker=<>,</>
set foldmethod=marker
set backspace=indent,eol,start

" Plug 'neoclide/coc.nvim'
call plug#begin('~/.config/nvim/autoload/plugged')
Plug 'nvim-treesitter/nvim-treesitter'
Plug 'vim-airline/vim-airline-themes'
Plug 'vim-airline/vim-airline'
Plug 'karb94/neoscroll.nvim'
Plug 'nvim-lua/plenary.nvim'
Plug 'jiangmiao/auto-pairs'
Plug 'tpope/vim-commentary'
Plug 'sheerun/vim-polyglot'
Plug 'jacoborus/tender.vim'
Plug 'cocopon/iceberg.vim'
Plug 'scrooloose/NERDTree'
Plug 'alvan/vim-closetag'
Plug 'tpope/vim-fugitive'
Plug 'morhetz/gruvbox'
call plug#end()

" customizations
colorscheme habamax
let g:NERDTreeMinimal =1
let NERDTreeQuitOnOpen =1
let g:closetag_shortcut = '>'
let g:closetag_filenames = '*.html,*.xhtml'

" misc shortcuts
nmap 99 :e ~/.vimrc<CR>
nmap . :suspend <CR>
nmap nt :NERDTreeToggle<CR>
nmap qw :wq <CR>
nmap ms :w <CR>
nmap qq :q <CR>
nmap 88 :wa<CR>

" screen splitting
nmap vsp :vsplit <CR>
nmap sp :split <CR>

" tabs
nmap > :tabnew<CR>
nmap < :tabclose<CR>
nmap tn :tabnext<CR>
nmap tp :tabprevious<CR>
nmap tb :Telescope buffers<CR>
nmap tt :terminal<CR>
nmap mn :!cal<CR>

" folding
nmap fu za<CR>
nmap fr zR<CR>
nmap fm zM<CR>

" cursor oops
nmap cw <C-w>x <CR>
nmap cu <C-w><Up> <CR>
nmap cl <C-w><Left> <CR>
nmap cd <C-w><Down> <CR>
nmap cr <C-w><Right> <CR>

" git oops
nmap gl :!git log --oneline -n 5<CR>
nmap gb :!git branch --list<CR>
nmap gs :!git status <CR>

" build tools
nmap mk :!make <CR>
nmap mt :!make test <CR>
nmap mc :!make clean <CR>

