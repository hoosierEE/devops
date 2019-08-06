NB. get file and remove comments
f =: (#~'#'~:{.&>)cutLF fread'~/.ssh/config'

NB. just the hostnames
hosts =: ~.;(}.@cut each #~('Host '-:5{.]) every) f
