from loader import _


async def start_message():
    text = _("Приветствуем вас в Exodus Bot!\nВыберите язык.\n\nWelcome to Exodus "
                                        "Bot!\nSelect a language.")
    return text


async def menu_message():
    text = _("Меню")
    return text


async def text_help_menu_func_ru():
    text = '''
<b>Функция бота:</b> 

Бот формирует референтный список людей, связанных взаимными p2p (peer to peer) намерениями о взаимопомощи не ограниченный числом участников. 

Список формируется по принципу взаимного поручительства (Арвут Ададит, иврит), который столетиями эффективно используется в этнических сообществах. 

<i>«Арвут» образовано от глагола «леарев» – «смешивать», «замешивать», «вмешивать». «Ададит» – «двусторонняя, взаимная (ответственность)». Получается, что «арвут ададит» – взаимная «вмешанность» друг в друга.</i>

Пользователь может начать создавать собственный список или присоединиться к уже существующему.

Для создания списка  доверия необходимо формализовать существующие отношения с теми, кого пользователь знает лично – "friends and family". 
А они, в свою очередь, делают то же и список расширяется автоматически. 
Это делается адресной рассылкой персонального приглашения: "я намереваюсь помочь тебе в случае необходимости условной суммой в 100 евро и рассчитываю на взаимность".

При клике на ссылку происходит включение участников в трастовый список как лично подтвержденная договоренность и автоматически дополняется по принципу "друг моего друга – мой друг". 


Таким образом формируется "общий пул намерений" участников сети. 

Например, если в списке 1000 участников, то величина "пула" составит 100.000 евро. Это по сути потенциально заявленный ресурс трастового списка для решения общих актуальных задач, от взаимопомощи до инициатив и прямой кооперации. 

—
<b>Важно:</b> Следует понимать, что задача пользователей сформировать как можно больший список участников. 
Список растет гиперболически, а значит общий пул и возможности каждого участника соответственно возрастут. 

Все коммуникации участников списка происходят вне бота.  
Бот не является платежным или расчетным инструментом и выполняет лишь функцию проявления трастового списка. 

В текущем боте пользователь может оповестить участников списка про необходимость экстренной помощи и указать ссылку, где происходит общение.

Трастовый список является необходимым, но недостаточным условием для возникновения “сети”. Децентрализованная трастовая сеть возникает как следствие деятельности участников трастового списка при возникновении события, требующего участия каждого. 

Для обеспечения взаимодействия между участниками списка разработан бот @exodus_commitbot, описанный отдельно.

Бот работает на русском, английском и сербском языке, выбор языка осуществляется в меню “НАСТРОЙКИ”   
    '''

    return text


async def text_help_about_menu_ru():
    text = '''
<b>Меню бота</b>

<b>СГЕНЕРИРОВАТЬ ССЫЛКУ.</b>
Выдает уникальную ссылку пользователя, которую нужно разослать своим друзьям для приглашения новых участников или чтобы подтвердить прямую связь с теми, кто уже есть в боте. Клик на ссылку и подтверждение связи вносит вас и вашего друга в список участников референтной сети, с которыми есть личная договоренность. 

<b>СПИСОК:</b>
Показывает прирост общего пула с момента предыдущего входа в бот.

<b>ГРАФ СЕТИ:</b>
Выдает визуальный граф сети, количество участников и количество прямых связей.

<b>ПОКАЗАТЬ СПИСОК:</b>
Показывает список всех участников сети, в верхней части которого пользователи, с которыми у вас есть личное подтверждение связи. Про каждого участника по его номеру в списке можно посмотреть, через кого он с вами связан.

<b>ЧЕРНЫЙ СПИСОК:</b>
Каждый может в одностороннем порядке отозвать свое намерение. Все участники списка будут оповещены проинформированы об этом.

<b>SOS / INFO:</b>
Вы можете проинформировать всех участников списка и прикрепить ссылку для коммуникации. Все коммуникации и взаимодействия осуществляются вне бота.

<b>НАСТРОЙКИ:</b>
Здесь можно выбрать один из рабочих языков для бота. Кнопка логин/пароль не активна до момента появления веб интерфейса. 

<b>FAQ:</b>
Справочная информация о работе бота и описание меню.

    '''

    return text


async def text_help_menu_func_en():
    text = '''
<b>Bot function:</b>

The bot forms a reference list of people connected by mutual p2p (peer to peer) intentions for mutual assistance, not limited by the number of participants.

The list is formed according to the principle of mutual guarantee (Arvut Adadit) (Hebrew).
“Arvut” is formed from the verb “learev” - “to mix”, “to knead”, “to intervene”. "Adadit" - "bilateral, mutual (responsibility)". It turns out that “arvut adadit” is a mutual “interference” with each other.

The user can start creating his own list or join an existing one.

To create a trust list, it is necessary to formalize the existing relationship with those whom the user knows personally - "friends and family". They, in turn, do the same and the list expands automatically.
This is done by direct mailing of a personal invitation: "I intend to help you, if necessary, with a conditional amount of 100 euros and I look forward to reciprocity."

When you click on the link, participants are included in each other's reference lists of two types - personally confirmed and automatically generated according to the principle "each other is my friend".

Thus, a "common pool of intentions" of network participants is formed.

<i>For example, if there are 1000 participants in the list, then the size of the "pool" will be 100,000 euros. It is, in fact, a potentially declared resource of the trust list for solving common urgent problems, from mutual assistance to initiatives and direct cooperation.</i>

<b>Important:</b> It should be understood that the task of users is to form the largest possible list of participants associated with "mutual guarantees".
Such a list will begin to grow hyperbolically, which means that the total pool and the capabilities of each participant will increase accordingly.

All communications of the list members take place outside the bot.
The bot is not a payment or settlement instrument and only serves as a manifestation of the trust list of participants.

A list of trust is a necessary but not sufficient condition for the emergence of a “network”. A decentralized trust network arises as a consequence of the activities of members of the trust list when an event occurs that requires everyone to participate.

In the current bot, the user can notify the members of the list about the need for emergency assistance and indicate the link where the communication takes place (in the menu, the "SOS / INFO" button).

To ensure interaction between members of the list, the @exodus_commitbot bot, described separately, has been developed.

<b>Language:</b> The bot works in several languages. The choice of language takes place in the "SETTINGS" menu.        
            '''

    return text


async def text_help_about_menu_en():
    text = '''
<b>Bot menu:</b>

<b>GENERATE LINK:</b>
Gives a unique user link that needs to be sent to your friends to invite new members or to confirm a direct connection with those who are already in the bot.  
Clicking on the link and confirming the connection brings you and your friend to the top of the list of members of the reference network with whom there is a personal agreement.

<b>LIST:</b>
Shows the growth of the total pool since the last login to the bot

<b>NETWORK GRAPH:</b>
Displays a visual graph of the network, the number of participants and the number of direct connections.

<b>SHOW LIST:</b>
Shows a list of all network members, at the top of which are users with whom you have a personal confirmation of communication.  
For each participant, by his number in the list, you can see through which shortest chain of direct contacts he is connected with you.

<b>BLACK LIST:</b>
Еeveryone can unilaterally withdraw their intention. All members of the list will be notified of this.

<b>SOS/INFO:</b>
You can inform all the participants of the list and attach a link for communication. All communications and interactions take place outside the bot.

<b>SETTINGS:</b> 
Here you can choose one of the working languages for the bot and in the future set a login/password for the platform on which decentralized interaction services are developed.  Login / password are not active now.

<b>FAQ:</b> 
Background information about the bot and a description of the menu.   
            '''

    return text


async def text_help_menu_func_sr():
    text = '''
<b>Bot funkcija:</b>

Bot čini referentnu listu ljudi povezanih međusobnim p2p (peer to peer) namjerama za uzajamnu pomoć, ne ograničavajući se na broj učesnika.

Popis je formiran prema principu uzajamnog jamstva (Arvut Adadit) (hebrejski), koji se stoljećima efikasno koristi u etničkim zajednicama.

„Arvut“ je nastao od glagola „learev“ - „miješati“, „mijesiti“, „intervenirati“. "Adadit" - "bilateralno, uzajamno (odgovornost)". Ispostavilo se da je "arvut adadit" uzajamno "miješanje" jedni s drugima.

Korisnik može započeti stvaranje vlastite liste ili se pridružiti postojećoj.

Za stvaranje liste povjerenja potrebno je formalizirati postojeći odnos s onima koje korisnik osobno poznaje - „prijateljima i porodicom“. Oni zauzvrat čine isto i lista se automatski proširuje.
To se postiže izravnom poštom na lični poziv: "Namjeravam vam pomoći, ako je potrebno, uslovnim iznosom od 100 eura i radujem se uzajamnosti."

Kada kliknete na vezu, sudionici se uključuju u međusobne referentne liste dviju vrsta - lično potvrđene i automatski generirane u skladu sa principom "jedni drugima su prijatelji".

Tako se formira „zajednički fond namjera“ sudionika mreže.

<i>Na primjer, ako na listi ima 1000 sudionika, tada će veličina "bazena" iznositi 100 000 eura. To je zapravo potencijalno deklarirani resurs liste povjerenja za rješavanje zajedničkih hitnih problema, od uzajamne pomoći do inicijativa i direktne suradnje.</i>

<b>Važno:</b> Treba shvatiti da je zadatak korisnika da formiraju najveću moguću listu sudionika povezanih s "uzajamnim garancijama".
Takva lista počet će hiperbolički rasti, što znači da će se ukupan fond i mogućnosti svakog sudionika povećavati u skladu s tim.

Sve komunikacije članova liste odvijaju se izvan bota.
Bot nije instrument plaćanja ili poravnanja i služi samo kao manifestacija liste povjerenja sudionika.

Lista povjerenja je neophodan, ali ne i dovoljan uvjet za pojavu „mreže“. Decentralizirana mreža povjerenja nastaje kao posljedica aktivnosti članova liste povjerenja kada se dogodi događaj koji zahtijeva da svi sudjeluju.

U trenutnom botu korisnik može obavijestiti članove liste o potrebi hitne pomoći i naznačiti vezu na kojoj se odvija komunikacija (u izborniku, gumb "SOS / INFO").

Da bi se osigurala interakcija između članova popisa, razvijen je bot @exodus_commitbot, opisan odvojeno.

<b>Jezik:</b> Bot radi na nekoliko jezika. Izbor jezika vrši se u izborniku "POSTAVKE".
            '''

    return text


async def text_help_about_menu_sr():
    text = '''
<b>BOT MENI:</b>

<b>GENERATI LINK:</b>
Daje jedinstvenu korisničku vezu koju treba poslati prijateljima kako biste pozvali nove članove ili potvrdili direktnu vezu s onima koji su već u botu.  Klik na vezu i potvrda veze dovodi vas i vašeg prijatelja na vrh liste članova referentne mreže s kojima postoji lični dogovor.

<b>LISTA:</b>
Prikazuje porast ukupnog fonda od posljednje prijave botu u obliku:
 Prethodna veličina bazena = 2500 €
 Trenutna veličina bazena = 2700 €
 Povećajte 200 €

<b>MREŽNI GRAF:</b>
Prikazuje grafikon vizuelne mreže, u kojem su korisnici uključeni na listu osobno potvrđenih kontakata označeni crvenom bojom, a svi ostali sudionici povezani s vama indirektno preko njegovih prijatelja i „prijatelja prijatelja“ plavom bojom

<b>SHOW LIST:</b>
Prikazuje listu svih članova mreže, na vrhu kojih su korisnici s kojima imate ličnu potvrdu komunikacije.  Za svakog učesnika, prema njegovom broju na listi, možete vidjeti preko kojeg je najkraćeg lanca direktnih kontakata povezan s vama.

<b>CRNA LISTA:</b>
Svi mogu jednostrano prekinuti vezu sa bilo kojim od korisnika sa liste.  Svi sudionici koji su direktno ili indirektno povezani s vama bit će obaviješteni o tome.  Ovdje se možete ponovo povezati i vratiti osobu na opću listu.  Ako ste osobu stavili na crni spisak, neće je moći direktno kontaktirati dok je ne vratite.

<b>SOS / INFO:</b>
Salje informativnu poruku svim članovima vašeg popisa.  Poruka može sadržavati vezu na pozivnicu za raspravu o općoj temi ili zahtjev za pomoć.  Sve komunikacije i interakcije odvijaju se izvan bota.

<b>POSTAVKE:</b>
Ovdje možete odabrati jedan od radnih jezika za bota i u budućnosti postaviti korisničko ime / lozinku za platformu na kojoj se razvijaju decentralizirane usluge interakcije.  Prijava / lozinka nisu sada aktivni.

<b>FAQ:</b>
Pozadinske informacije o botu i opis menija.
            '''

    return text