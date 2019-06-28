# Discord Minefield Bot

## What is it?
Discord Minefield is a Discord bot that allows you to play Python-coded games on Discord!
And yes, we code ourselves the games!

This bot was made for Discord Hack Week event in 2019, but we will keep the development active.

**Current games on the bot:**
- Minesweeper
  - Spoiler version (the one that you see everywhere on Discord)
  - Interactive version (send tile coordinates, reveal tiles, flag tiles, win and lose, just like a **true minesweeper game**!)
- Rock Paper Scissors (we wanted to code a Hunt the Wumpus game (but Catch instead of Hunt) but we didn't have enough time...)
- More coming soon!

N.B.: Minesweeper Interactive version is currently in beta and can have some bugs. We're working on the code to squash as many bugs as we can.

## Can I add it on my server?
Yes! [Click to invite the bot](https://discordapp.com/oauth2/authorize?client_id=594134805692547103&scope=bot&permissions=1409674320)
Consider joining our support server, maybe in the future you may get some extra stuff, idk...
[Server link](https://discord.gg/SxyWxWq)


## What are the commands?
They are listed below

**Games command**:
- `ms.minesweeper [amount of mines]` -> Start a Minesweeper game and generates a grid with \[amount of mines]
- `ms.rockgame` -> Start a Rock Paper Scissors game by asking first the amount of points (if incorrect, will be 10) and then playing by using reactions. Don't go too fast or the bot may slow down

**Other commands**:
- `ms.game_rules [game]` -> See the rules of a game. If the game is not given, will show all the games available on the bot.
- `ms.help [command]` -> Shows the list of commands, as well as syntax and aliases, including the help of help command (usefulness = 0.00000000000000000001%)
- `ms.credits` or `ms.about` -> Shows info about the bot and its creators. *Seriously, does anyone read this?*
- `ms.bug_report` -> Opens an interactive window where you can report a bug to us via Discord. Has a 6-hour cooldown per user
- `ms.suggestion <suggestion>` -> Will send a suggestion to the devs. If not given, will open an interactive window where you type in your suggestion. Has a 24-hour cooldown per user
