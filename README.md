# The Resistance: Avalon - Discord Edition
*Discord bot built using discord.py library. Original game by Don Eskridge.*

#Technical Requirements
*Only if you wish to download the source code and host your own copy of Avalon*
- Python 3.5
- pip - https://pip.pypa.io/en/stable/installing
- discordpy - https://github.com/Rapptz/discord.py  
`python3 -pip install -U discord.py`

# Rules
*Information in this section drawn from a combination of the game's manual, Wikipedia and theresistanceonline.com*

**The Resistance: Avalon** is a variant of **The Resistance**. It is similar in structure to party games such as Mafia and Werewolf, where a small, secret group of informed players attempt to disrupt a larger uninformed group, while the larger group attempts to identify the traitors and eliminate them. The Resistance uses slightly different mechanics from similar games, and was designed to avoid player elimination and increase available information for player decisions.

Avalon is a game of hidden loyalty. Players are either Loyal Servants of Arthur fighting for Goodness and honor or aligned with the Evil ways of Mordred. Good wins the game by successfully completing three Quests. Evil wins if three Quests end in failure. Evil can also win by assassinating Merlin at game's end or if a Quest cannot be undertaken.

- The game requires between five and ten players.
- Approximately one third of the players are randomly chosen as **Evil**; the rest are **Good**. This depends on the player count.
- Evil players have knowledge of who their fellow evil players are. The Good players do not have any additional information.
- The game consists of up to five rounds called Quests.
- Each quest has a leader. The leader proposes a quest party of a certain size as determined by the game, which the group approves by public vote.
- The leader for the first quest is randomly determined, it will then pass in a sequential fashion as determined by the player list.
- If the group does not approve the quest by a simple majority, leadership passes to the next player.
- If the group cannot approve a quest party after five attempts, Evil wins.
- Once a mission team is chosen, it votes by secret ballot whether the mission succeeds or fails.
- Good will always vote for success and are unable to fail, but Evil has the option of voting for success or failure.
- It usually only takes one traitor to sabotage a quest, but in games of 7 or more the fourth quest will require two fails.
- If three quests succeed, Good wins. If three fail, Evil wins.
- In the event of a Good victory, a character known as the assassin will choose one person to assassinate. If Merlin is correctly identified and assassinated, Evil wins. 

# Special Roles

**Good**  
- Merlin - Merlin has knowledge of all the Evil players in the game (except Mordred). He must lead the forces of good, but do so with subtlety lest he be identified by the Assassin.
- Percival - Has knowledge of who Merlin is. If Morgana is in the game, Morgana will also appear as Merlin. Percival must carefully determine which is the true Merlin and condemn the imposter Morgana.

**Evil**  
- The Assassin - If Good wins, if the Assassin is able to correctly identify Merlin- Evil will win instead.
- Morgana - Appears to Percival as Merlin. Must attempt to turn Percival against the true Merlin.
- Mordred - The Big Bad. Fully hidden. Merlin does not know who the Mordred player is.

# Commands
- `!avalon` - Starts the game.
- `!help` - Direct messages the user a link to this page.
- `!stop` - End the currently running game.
- `!join` - Used to join the game during the login phase.
- `!party` - Used by the leader to propose a party during the team building phase.
- `!approve/!reject` - Used to approve or reject a party during the team building phase.
- `!success/!fail` - Used to succeed or fail a quest during the secret vote phase.
- `!assassinate` - Used by the Assassin in the event of a Good victory to assassinate a member of the game. This command does not have any input verification and only allows you **one** try. Ensure that you @tag the correct person!

# Coming Soon
- Oberon.
- Custom discord version of Lancelot.
- Ability to select exactly which roles come into play.

# Known Issues/Limitations
- When two or more players message the bot at the same time, the bot is only able to process one of the messages.

# Original Rulebook
The original game rules can be found at http://upload.snakesandlattes.com/rules/r/ResistanceAvalon.pdf
