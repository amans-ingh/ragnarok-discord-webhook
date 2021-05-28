from dhooks import Webhook, Embed
import csv

hook_pre = Webhook("https://discord.com/api/webhooks/831522858177265664/fEnk2v"
                   "kiaHK6iKl4XRAxAYNkZ091LT8_TugJuoVsrHULI4iR2HymQhN8M579586JQN82")
hook_post = Webhook("https://discord.com/api/webhooks/831523233857273866/Zzxm7"
                    "NJaWPT1Wk3QT51TMBP3xXmu02lnpi3riemSjAz7cN8ejEmpLDe31MYZ71i2BIVq")


class RagnarokBot:
    def pre_match(self, team1, team2, time, channel, color, date):
        title = team1 + ' vs ' + team2
        if title == "MAG vs Team FL4RE":
            join_time = '8:20 PM'
            match_time = '8:30 PM'
        else:
            join_time = str(time-1) + ':50 PM'
            match_time = str(time) + ':00 PM'
        fields = ['Voice Channel Name', 'Join Time', 'Match Time']
        value = [channel, date + ' ' + join_time, date + ' ' + match_time]
        embed = Embed(
            title=title,
            description='Captains of both the teams ' + team1 + ' and ' + team2 + ' are required to join '
                        'the voice channel \"' + channel + '\" for map veto and lobby invite.',
            color=color,
        )
        i = 0
        for field in fields:
            embed.add_field(name=field, value=value[i])
            i = i + 1
        hook_pre.send(embed=embed)

    def post_match(self, team1, team2, winner, map, color, score, mvp):
        title = 'Match Result - ' + team1 + ' vs ' + team2
        fields = ['Winner', 'Score', 'Map Played']
        value = [winner, score, map]
        embed = Embed(
            title=title,
            description=winner+' clinched the match with the score ' + score + ' and the most valuable player of the match was ' + mvp + '.',
            color=color
        )
        i = 0
        for field in fields:
            embed.add_field(name=field, value=value[i])
            i = i + 1
        hook_post.send(embed=embed)

    def schedule(self, field, values, date):
        embed = Embed(
            title='Match Schedule for ' + date,
            description='Match schedule for ' + date + ' is given below. All the participants are requested to join '
                                                      'voice channel on time.',
            color=0xFF6969
        )
        embed.add_field(name='Match', value=field, inline=True)
        embed.add_field(name='Time', value=values, inline=True)
        hook_pre.send(embed=embed)



csgo = RagnarokBot()
option = input("notify(n) or result(r) or schedule(s): ")
if option == '0' or option == 'n' or option == 'notify':
    day = str(input('Enter day: '))
    time = str(input('Enter time: '))
    with open('details.csv', 'r') as details:
        csv_read = csv.reader(details, delimiter=',')
        for row in csv_read:
            if row[1]==day and row[2]==time:
                team1 = row[3]
                team2 = row[4]
                match_time = int(row[2])
                if int(row[0]) % 2 == 0:
                    channel = 'Lobby 2 CSGO'
                    color = 0xA500FF
                else:
                    channel = 'Lobby 1 CSGO'
                    color = 0x00FF00
                date_num = int(day) + 14
                date = str(date_num) + 'th April'
                csgo.pre_match(team1, team2, match_time, channel, color, date)
elif option == '1' or option == 'r' or option == 'result':
    match_number = input("Enter Match number: ")
    with open('details.csv', 'r') as details:
        csv_read = csv.reader(details, delimiter=',')
        for row in csv_read:
            if row[0] == match_number:
                if row[6]:
                    team1 = row[3]
                    team2 = row[4]
                    winner = row[6]
                    map = row[9]
                    mvp = row[10]
                    score = row[7]
                    if int(row[0]) % 2 == 0:
                        color = 0xA500FF
                    else:
                        color = 0x00FF00
                    csgo.post_match(team1, team2, winner, map, color, score, mvp)
elif option == '2' or option == 's' or option == 'schedule':
    day_number = input("Enter day: ")
    date = str(int(day_number) + 14) + 'th April'
    with open('details.csv', 'r') as details:
        csv_read = csv.reader(details, delimiter=',')
        fields = []
        field = ''
        value = []
        values = ''
        for row in csv_read:
            if row[1] == day_number:
                match = row[3] + ' vs ' + row[4]
                match_time = row[2] + ':00 PM '
                fields.append(match)
                value.append(match_time)
        for val in value:
            values = values + val + '\n'
        for fiel in fields:
            field = field + fiel + '\n'
        csgo.schedule(field, values, date)
