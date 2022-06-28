create table if not exists news (
    id integer not NULL primary key AUTOINCREMENT,
    Feed text,
    Title text,
    Link text,
    Date text,
    Description text,
    Source text,
    Media text,
    GUID text,
    Url text,
    LocalImgLink text
);