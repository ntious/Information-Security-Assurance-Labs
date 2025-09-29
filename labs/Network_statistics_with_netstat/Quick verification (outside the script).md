# TCP listeners (needs sudo for PID/Program)
sudo ss -ltnp | grep -E '(:3306\b|:33060\b)'
# Active TCP/UDP endpoints
sudo ss -tunap | grep -E '(:3306\b|:33060\b|mysqld)'
# UNIX sockets (if socket-only)
sudo ss -xap | grep -i mysql
# Force a TCP entry (then re-run the first/second command)
mysql -h 127.0.0.1 -P 3306 -u root -p   # or use 33060 if that’s the listener
