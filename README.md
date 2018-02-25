# asyncssh 129

Steps to reproduce:

1. Run the TCP server: `./tcp`
2. Run the SSH server: `python server.py`
3. Run the client: `python client.py`

Now that may not quite do it. The error is intermittent. For me, this command
seems to cause the error consistently:

```
for x in {1..100}; do python client.py ; done
```

It also spikes my CPU usage while it runs, so be warned.

The `output.log` file contains sample logs. The interesting part are the `CONN
EXCEPTION` logs.
