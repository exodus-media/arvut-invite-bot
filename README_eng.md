[Русский](README.md)

## Bot function:

The bot forms a reference list of people connected by mutual p2p (peer to peer) intentions for mutual assistance, not limited by the number of participants.

The list is formed according to the principle of mutual guarantee (Arvut Adadit) (Hebrew).
“Arvut” is formed from the verb “learev” - “to mix”, “to knead”, “to intervene”. "Adadit" - "bilateral, mutual (responsibility)". It turns out that “arvut adadit” is a mutual “interference” with each other.

The user can start creating his own list or join an existing one.

To create a trust list, it is necessary to formalize the existing relationship with those whom the user knows personally - "friends and family". They, in turn, do the same and the list expands automatically.
This is done by direct mailing of a personal invitation: "I intend to help you, if necessary, with a conditional amount of 100 euros and I look forward to reciprocity."

When you click on the link, participants are included in each other's reference lists of two types - personally confirmed and automatically generated according to the principle "each other is my friend".

Thus, a "common pool of intentions" of network participants is formed.

For example, if there are 1000 participants in the list, then the size of the "pool" will be 100,000 euros. It is, in fact, a potentially declared resource of the trust list for solving common urgent problems, from mutual assistance to initiatives and direct cooperation.

Important: It should be understood that the task of users is to form the largest possible list of participants associated with "mutual guarantees".
Such a list will begin to grow hyperbolically, which means that the total pool and the capabilities of each participant will increase accordingly.

All communications of the list members take place outside the bot.
The bot is not a payment or settlement instrument and only serves as a manifestation of the trust list of participants.

A list of trust is a necessary but not sufficient condition for the emergence of a “network”. A decentralized trust network arises as a consequence of the activities of members of the trust list when an event occurs that requires everyone to participate.

In the current bot, the user can notify the members of the list about the need for emergency assistance and indicate the link where the communication takes place (in the menu, the "SOS / INFO" button).

To ensure interaction between members of the list, the @exodus_commitbot bot, described separately, has been developed.

Language: The bot works in several languages. The choice of language takes place in the "SETTINGS" menu.

## Bot menu:

GENERATE LINK:  Gives a unique user link that needs to be sent to your friends to invite new members or to confirm a direct connection with those who are already in the bot.  Clicking on the link and confirming the connection brings you and your friend to the top of the list of members of the reference network with whom there is a personal agreement.

LIST: Shows the growth of the total pool since the last login to the bot.

NETWORK GRAPH: displays a visual graph of the network, the number of participants and the number of direct connections.

SHOW LIST: shows a list of all network members, at the top of which are users with whom you have a personal confirmation of communication.  For each participant, by his number in the list, you can see through which shortest chain of direct contacts he is connected with you.

BLACK LIST: Еeveryone can unilaterally withdraw their intention. All members of the list will be notified of this.

SOS / INFO: You can inform all the participants of the list and attach a link for communication. All communications and interactions take place outside the bot.

SETTINGS: Here you can choose one of the working languages for the bot and in the future set a login / password for the platform on which decentralized interaction services are developed.  Login / password are not active now.

FAQ: Background information about the bot and a description of the menu.

## Deploy the bot at your server

To start the bot, you need to:
- clone the repository to the desired location (local computer or remote server);
- prepare a PostgreSQL database. Namely, install PostgreSQL on your server, create a user and password, create a database. Remember this data;
- create a config file.py in the data directory by analogy with the file config.test.py by filling in the current API_TOKEN and DATABASE_URL_PG;
- when using the bot locally on your home computer, set it in the file config.py DEBUG = True. If the bot is run on an industrial scale on the server, then specify DEBUG = False and at the same time fill in the values of WEBHOOK_, which are generated according to the instructions for WEBHOOK;
- install the necessary modules and packages for the bot using the command "pip install-r requirements.txt";
- install "sudo apt install systemd" (if it is not already installed);
- install redis-server using the command " sudo apt install redis-server";
- start / disable redis-server using the commands "sudo systemctl start redis-server" / " sudo systemctl enable redis-server";
- set the multi-language bot, being in the root of the project " pybabel compile-d locales -D testbot"
- launch app.py (it is advisable to add this script for execution via systemctl).