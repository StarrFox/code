# pydb

## stores

```a

pydb (encoded) version (2) table header

table header:
primary key indexes (2)+
collum info +

collum info:
size (2)
sized string name
type (2)

sized string:
size (4)
data (utf-8)

data+

data is just a stream of collum types
```
