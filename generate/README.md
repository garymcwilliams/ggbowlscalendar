# Generate Bowls Data

## Ruunning

Simplest way to run this is to do

``` bash
poetry shell
cd generate
python generate.py
```

## Configuration

Create a file called `matches.txt`, from one of the samples. This is a simple line based file, with the following structure:

line 1: is the `me:` data for the `yaml` file.
line 2: is the name of the `yaml` file to be created
line 3: is the default `duration` for a match of this team
line 4: is the `starting date` for the first league match
line 5: is the `default start time` for matches in this league
Line 6+: if a simpel one-line per match showing `home/away` `opposition code` `date offset` from the prvious match. NOTE that the first match should have offset 0 to match the `starting date` defined above.
