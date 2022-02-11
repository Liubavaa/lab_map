# Main.py

Module operate with data that contain information films titles, year and location of filming. Create web-map(HTML file).
The map show information about the locations of films that were shot in a given year.

## Map

It has two additional layers. One contains 1 red marker indicating given coordinates and 10 black markers containing the address and movies titles that were shot there in the given year. The other layer contains lines that connect the red marker with the black ones and the distance between the markers appears when hovering over lines.

## Usage

```bash
python3 main.py 2015 49.841952 24.0315921 'locations.list'
```
![image](https://user-images.githubusercontent.com/92572643/153666003-b03259a4-6279-4e98-9472-904ca67d2825.png)

### P.S.
There are some locations, which coordinates program can't find, as a result some of they overlap, but if you zoom a little, you will see them separately.
