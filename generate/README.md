# Generate Bowls Data

## Ruunning

Simplest way to run this is to do

``` bash
poetry shell
cd generate
./generate.py
```

## Configuration

Create a file called `matches.txt`, from one of the samples. This is a simple line based file, with the following structure:

line 1: is the `me:` data for the `yaml` file.
line 2: is the name of the base `yaml` file to be created. this will be appended with '_games_' plus the YEAR from line 4.
line 3: is the default `duration` for a match of this team
line 4: is the `starting date` for the first league match
line 5: is the `default start time` for matches in this league
Line 6+: if a simple one-line per match showing `home/away` `opposition code` `date offset` from the previous match. NOTE that the first match should have offset 0 to match the `starting date` defined above. The `opposition code` can have a `-A` (etc) added to reflect, for example, Belmont A.
