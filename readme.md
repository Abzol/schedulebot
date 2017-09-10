schedulebot is a small python3.4 discord bot written using
[discordpy](https://github.com/Rapptz/discord.py).

You hook it up to a server, prove it some normal permissions, and
then invoke `!setup [user [user ..]]` and `!raid [mode day [desc]]`
(as it was originally meant to plan Final Fantasy XIV raids).

After that users can report if they'll be present with `+day`, gone with
`-day` or still unknown with `?day`, as well as giving a reason
