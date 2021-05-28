from dhooks import Webhook, Embed
import csv

hook_pre = Webhook("https://discord.com/api/webhooks/831846552502534164/8jK2kmZ7ivYSw0ptxBnxIP_ukvAcfYjDPg74hXURf-nmkaMG2cK78LGj-t3Oaep8F8a9")
hook_post = Webhook("https://discord.com/api/webhooks/832198942052974653/f7HsYkzaQ-gJPiU9qLX7SmU3Ve1WrnWnFJd0iJEifZEs29TwyNBfIRlrEKcRdSafQxeg")


class RagnarokBot:
    def pre_match(self, team1, team2, time, channel, color, date):
        title = team1 + ' vs ' + team2
        if title == "MAG vs HighTableGaming":
            join_time = '5:20 PM'
            match_time = '5:30 PM'
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

    def post_match(self, team1, team2, winner, map, color, score):
        title = 'Match Result - ' + team1 + ' vs ' + team2
        fields = ['Winner', 'Score', 'Map Played']
        value = [winner, score, map]
        embed = Embed(
            title=title,
            description=winner+' clinched the match with the score ' + score + ' on ' + map,
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
            # description='The map will be chosen by map veto system, using ABAB method. '
            #             'Join the specified voice channel to get invited to the lobby for the match. '
            #             'The voice channel name and time to join will be specified by the Ragnarok bot '
            #             'before your match.',
            description='Match schedule is given below, any team having problems can approach admins '
                        'before midnight. The schedule for later days will be declared after the completion of matches '
                        'in this round.',
            color=0xFF6969
        )
        embed.add_field(name='Match', value=field, inline=True)
        embed.add_field(name='Time', value=values, inline=True)
        hook_pre.send(embed=embed)


valo = RagnarokBot()
option = input("notify(n) or result(r) or schedule(s): ")
if option == '0' or option == 'n' or option == 'notify':
    day = str(input('Enter day: '))
    time = str(input('Enter time: '))
    with open('valo.csv', 'r') as details:
        csv_read = csv.reader(details, delimiter=',')
        color = 0xA5000F
        i = 1
        for row in csv_read:
            if row[1]==day and row[2]==time and row[3] and row[4]:
                team1 = row[3]
                team2 = row[4]
                match_time = int(row[2])
                channel = 'Lobby ' + str(i) + ' Valo'
                i = i + 1
                color = color + 0x000F00
                date_num = int(day) + 14
                date = str(date_num) + 'th April'
                valo.pre_match(team1, team2, match_time, channel, color, date)
elif option == '1' or option == 'r' or option == 'result':
    match_number = input("Enter Match number: ")
    with open('valo.csv', 'r') as details:
        csv_read = csv.reader(details, delimiter=',')
        for row in csv_read:
            if row[0] == match_number and row[3] and row[4] and row[5]:
                team1 = row[3]
                team2 = row[4]
                winner = row[5]
                map = row[7]
                score = row[6]
                color = 0xA500FF
                valo.post_match(team1, team2, winner, map, color, score)
elif option == '2' or option == 's' or option == 'schedule':
    day_number = input("Enter day: ")
    date = str(int(day_number) + 14) + 'th April'
    with open('valo.csv', 'r') as details:
        csv_read = csv.reader(details, delimiter=',')
        fields = []
        field = ''
        value = []
        values = ''
        for row in csv_read:
            if row[1] == day_number and row[3] and row[4]:
                if row[3] == 'MAG':
                    match_time = '5:30 PM'
                else:
                    match_time = row[2] + ':00 PM '
                match = row[3] + ' vs ' + row[4]
                fields.append(match)
                value.append(match_time)
        for val in value:
            values = values + val + '\n'
        for fiel in fields:
            field = field + fiel + '\n'
        print(field)
        print(values)
        valo.schedule(field, values, date)
