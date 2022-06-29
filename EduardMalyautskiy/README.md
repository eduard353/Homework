# RSS reader
RSS reader is a command-line utility which receives RSS URL and prints results in human-readable format.

## Installation and usage
It is recommended to use a python virtual environment.
How use virtual environment you can read [here](https://docs.python.org/3/library/venv.html). 

After download RSS reader you can install it by:
```
pip setup.py install
```
and use by:
```
rss_reader ...
```
or you can change directory to directory with `rss_reader.py` file:
```
cd rss_reader
```
install requirements
```
pip install -r requirements.txt
```
and use:
```
python rss_reader.py ...
```
You can read the help of RSS reader using the command:
```
rss_reader --help
```
or
```
python rss_reader.py --help
```
RSS reader provide the following interface:
```
usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--colorize] [--limit LIMIT] [--date DATE] [--to_html [PATH]] [--to_pdf [PATH]] [--clear_cache] [source]

Pure Python command-line RSS reader.

positional arguments:
  source            RSS URL

optional arguments:
  -h, --help        show this help message and exit
  --version         show program's version number and exit
  --json            Print result as JSON in stdout
  --verbose         Outputs verbose status messages
  --colorize        That will print the result of the utility in colorized mode
  --limit LIMIT     Limit news topics if this parameter provided
  --date DATE       It should take a date in YearMonthDay format. For example: --date 20191020. The cashed news can be read with it. The new from the specified day will be printed out. If the news are not found return an error.
  --to_html [PATH]  Upload result to html-file in folder in PATH parameter, file name is current date with ms.
  --to_pdf [PATH]   Upload result to pdf-file in folder in PATH parameter, file name is current date with ms.
  --clear_cache     Delete data from cache DB.
```
Default output using follow structure:
```
------------------------------------------------------------
Feed:  Газета ВСЁ
Title:  Мост с зареки в центр находится в плачевном состоянии
Date:  2022.06.16
Link:  https://vse.sale/news/view/37514
Description:  Недавно отремонтированый мост, вновь в плохом состоянии и что бы оставить свою машину целой, приходится нарушать ПДД, а именно выезжать на встречную полосу.
Media:  http://vse.sale/files/news/2022/06/102375_1655367671.jpg
------------------------------------------------------------
```

In case of using `--json` argument RSS reader convert the news into JSON format. 
JSON contains follow data:
```json
{
        "Date": "",
        "Description": "",
        "Feed": "",
        "Link": "",
        "LocalImgLink": "",
        "Media": "",
        "Title": "",
        "Url": ""
    }
```
JSON keys description:

`Date` - date of article in %Y.%m.%f format, example `"2022.06.29"`

`Description` - description of article.

`Feed` - Feed title.

`Link` - Link to article.

`LocalImgLink` - path to local saved image.

`Media` - link to image.

`Title` - title of article.

`Url` - url of RSS feed.

## News caching.
For caching date used SQLite database, image saved to `images` folder.

SQLite database used followed schema:

```sql
create table if not exists news (
    id integer not NULL primary key AUTOINCREMENT,
    Feed text,
    Title text,
    Link text,
    Date text,
    Description text,
    Media text,
    Url text,
    LocalImgLink text
);
```

For clearing cache database you can use `--clear_cache` option.

RSS reader can save data in HTML and PDF formats. For it use `--to_html` and `--to_pdf` options with existing path.

RSS reader can colorize output data (default and json format). For it use `--colorize` option.

## Testing
For run RSS reader unit tests use:
```
python -m unittest parser_tests.py
```
