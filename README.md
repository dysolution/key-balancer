# Key Balancer 
An app to evaluate your music library's harmonic mixing options.

## Synopsis
Harmonic Mixing makes for smoother transitions between tracks, making sure
each track is related to the next either by being a "neighbor" on the Circle
of Fifths or its relative major or relative minor key.

Key Balancer reads the ID3 tags of your MP3s, looks at the TKEY attribute,
and prints out a sorted list of how many other tracks could be harmonically
mixed with a track in each key that matches at least one track in your
collection.

## Usage
In this example, your MP3 collection is in a directory inside your home
directory. Change the path as appropriate.
```
python key_balancer.py ~/mp3

# or on Windows:
python key_balancer.py "C:\Users\my_username\mp3"
```

You can also limit the search only to files within a specific BPM range:
```
python key_balancer.py ~/mp3 --bpm=125 --range=2  # matches 123 bpm to 127 bpm
python key_balancer.py ~/mp3 --bpm=128 --range=4  # matches 124 bpm to 132 bpm
```

## Output

![example output](img/sample_output.png?raw=true "Example Output")
