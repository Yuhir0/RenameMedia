## Rename Media

This scrip is thinked to automate the rename work, you can rename your series to fit next format. This format is the most common to add the metadata for differents players.

##### Format 

`Title S01 E01`
Where: 
- Title is the Title of the serie
- S01 is the season
- E01 is the episode

You can rename the media using:
python3 rename_media.py path="<path to the directory>"  name="<the name of the file to rename>" title="<the title for the serie>"

For example
```python
python3 rename_media.py path="/media/Series/Kimetsu no Yaiba"  name="[Publisher] Demon Slayer: Kimetsu no Yaiba - 01 (1080p).mkv" title="Kimetsu no Yaiba"
```

The result will be `/media/Series/Kimetsu no Yaiba/Kimetsu no Yaiba S01 E01.mkv`


### Parameters

- `path`: *Mandatory!!* The path to the directory that contains the chapter o chapters. May be full path or relative path.
- `title`: *Mandatoru!!* The title of the serie you would set.
- `name`: The name of the file to rename, inside the directory set on `path`, will be ignored if the `all` parameter is used.
- `all`: Values **yes** or **no**. If the parameter is not set is equal to say **no**. If is set as **yes** the scrip search for rename all files inside the directory. Ignoring hidden files. **If yo use the all parameter make sure the chapters are correctly ordered before execute the script**


### Seting by Season

To set the season you need to put the chuperts inside a season folder named `Season ##` (case insensitive) on the `##` will be double digit number like 01, `Season 01`

For example
```python
python3 rename_media.py path="/media/Series/Kimetsu no Yaiba/Season 03"  name="[Publisher] Demon Slayer: Kimetsu no Yaiba: Yukaku-hen - 01 (1080p).mkv" title="Kimetsu no Yaiba"
```

The result for this will be `/media/Series/Kimetsu no Yaiba/Season 03/Kimetsu no Yaiba S03 E01.mkv`