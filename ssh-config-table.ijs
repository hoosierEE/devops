row =: cut&>(cutLF;.1~'Host 'E.])fread'~/.ssh/config'
key =: a:-.~~.,{."1 row
val =: {:"1 row
idx =: {."1 key i.row
exit echo key,/:~3 :'(y{val) (y{idx) } a:#~1+#key'"0 i.#val