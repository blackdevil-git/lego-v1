inotifywait -q -m -e close_write --format %e lego.py |
while read events; do
  sudo python3 lego.py 
done