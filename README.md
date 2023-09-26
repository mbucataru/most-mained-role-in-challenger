<h3>A program that finds the most mained role in Challenger</h3>

<p>This works by iterating through each challenger player, checking their last 7 matches for their role, then returning
the most frequent one to our total counting array.</p>

<p>Once every player has been iterated through, the program prints the most frequent role from all of the most frequent 
roles of each player</p>

<p><strong>To use, download the repo and create api_key.txt with your API key</strong></p>

<p>Limitations:</p>
<ul>
    <li>Quite slow. Has to check each match history of each player.</li>
    <li>Only checks the first seven ranked matches. If a player has not played ranked
    in seven games, they are not included in the tally.</li>
    <li>Does not currently log the results, only prints. (TO-DO)</li>
</ul>

