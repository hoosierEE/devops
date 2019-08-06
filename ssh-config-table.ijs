NB. only works with "verbose" ssh_config file (e.g. each Host block is complete)
NB. this version DOES NOT WORK if you use wildcards for Host matching.

row =: cut&> ''"_^:('#'={.)each (cutLF;.1~'Host 'E.])fread'~/.ssh/config'
key =: a:-.~~.,{."1 row
val =: {:"1 row
idx =: {."1 key i.row
echo key,/:~3 :'(y{val) (y{idx) } a:#~1+#key'"0 i.#val
exit''