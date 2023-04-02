prefix = @prefix@
exec_prefix = @exec_prefix@
bindir = @bindir@

cexample: src/main.c
	$(CC) -Wall -O3 -o cexample src/main.c

clean:
	rm -f cexample

install: cexample
	install -d $(bindir)
	install -t $(bindir) cexample
