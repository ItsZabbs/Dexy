CREATE TABLE IF NOT EXISTS GuildData(
  GuildID bigint PRIMARY KEY,
  prefixes text [] default ARRAY['dexy']::text [],
  AliasText varchar [] default '{}',
  AliasSprites varchar [] default '{}'
);
