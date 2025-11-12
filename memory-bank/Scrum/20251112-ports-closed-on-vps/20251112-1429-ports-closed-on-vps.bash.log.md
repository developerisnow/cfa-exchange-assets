# Bash
```bash
# run tunnels
ois-cfa (deploy) ❯ ssh -N -L 15500:localhost:5000 -L 15808:localhost:8080 -L 15301:localhost:3001 -L 15302:localhost:3002 cfa1

# check locally (doesn't work)
ois-cfa (deploy) ❯ curl  http://localhost:15808/   13:58:52

curl: (52) Empty reply from server
ois-cfa (deploy) ❯ curl http://localhost:15301/    14:27:55
curl: (56) Recv failure: Connection reset by peer
ois-cfa (deploy) ❯ curl  http://localhost:15302/   14:28:09

curl: (56) Recv failure: Connection reset by peer
ois-cfa (deploy) ❯     

# check on cfa1 vps, expected work, but we see doesn't work - it explain why locally tunnels doesn't work help()

Last login: Wed Nov 12 10:47:06 2025 from 88.249.46.132
root@6001289-dq95453:~# curl localhost:3002
curl: (7) Failed to connect to localhost port 3002 after 1 ms: Couldn't connect to server
root@6001289-dq95453:~# curl localhost:3002
curl: (7) Failed to connect to localhost port 3002 after 1 ms: Couldn't connect to server
root@6001289-dq95453:~# curl localhost:8080
curl: (56) Recv failure: Connection reset by peer
root@6001289-dq95453:~# curl localhost:5000/health
Healthyroot@6001289-dq95453:~#

```