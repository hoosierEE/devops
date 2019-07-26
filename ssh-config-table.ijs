rows =: (<;.1~[:{."1(<'Host')=S:1])cut&.>cutLF fread'~/.ssh/config'
head =: ~.{.S:1 rows
pos =: {."1 head i.>>rows
r =: a:#~1+#head
item =: >1{::L:1 rows
exit echo }:"1 head, 3 :'(y{item)(y{pos)}r'"0 <:i.#item
