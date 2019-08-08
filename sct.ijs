file     =: a:-.~'#'taketo &.> cutLF fread'~/.ssh/config'   NB. strip comments
hosts    =: ~.;(}.@cut &.> #~('Host '-:5{.]) &>) file       NB. Host names (including wildcards)
attrs    =: ~.;deb@{.@cut &.> file                          NB. all attributes used in the file (including 'Host')
kv       =: split@cut&>file                                 NB. ,.(key ; values)
sections =: deb L:0 (<;.1~(<'Host ')=5&{.L:0)file           NB. Host: <...> groups (including wildcards)
rxfixup  =: ('.'&,&.>^:('*'(={.)&>])"0) hosts               NB. change leading '*' into '.*' so rxmatch doesn't complain
tab      =: (#attrs){."1 ,.hosts                            NB. empty table, prepopulated with hosts (attrs: column names)

NB. for Host in sections: put value at key unless value exists

hidx     =: hosts i.L:1}.@cut&.>{.&>sections                NB. indexes of hosts for attrs
aidx     =: ;@}.L:1 attrs i.L:1{.@cut L:0 sections          NB. attribute locations per section
params   =: }.L:1;L:1}.@cutL;0 sections                     NB. parameters for each section