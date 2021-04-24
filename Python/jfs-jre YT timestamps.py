from datetime import datetime

timestampDelimiter = ' '

url = 'https://www.youtube.com/watch?v=f_q4l-n2lhk'

summary ='''2:00 Josh says he doesn't give a shit what his trolls do anymore 
3:30 Josh says there's a lot of people botting and then says there's a lot of people planning on mass unsubbing 
4:00 fuck bitesize and anon 
4:40 Tactical soap 15% now! 
5:35 Josh says people will be pissed that he made the video 
7:50 Josh says someone pointed out that he has a lot of bots on his channel and mentions the subreddit and threatning to mass unsub 
9:50 Josh says he took a break and made his videos private for a social experiment 
11:30 Josh sent the cobraverse into a nasty tailspin and says everything is in his control 
12:10 Josh says he has people that really care about him and people have a problem with that 
13:20 Josh has more soap on the way and talks about tactical soap evening out the playing field 
15:00 Josh owns the trolls and thinks that they want him to stop making videos 
15:40 his videos are back on and his comments are back on also 
16:00 Josh doesn't monitise his videos because he smokes etc and talks about being harassed and Youtube does nothing. Josh talks about bots checking videos for monitisation 
17:30 Josh talks about flagging channels/videos harassing him and it goes to a bot and nothing happens 
19:25 Josh says his apartment isn't as dirty as it looks in the second documentary, he cleans it 
20:15 Josh says King Cobra is just a stage name 
20:50 Josh talks about snakes while getting ready to snort tobacco 
21:50 Josh is going to hang out with some friends after the video 
22:10 Josh says the trolls wish they could be him, thats why they steal his videos 
22:40 Josh says people have been helping him and he says he's in work mode and mentions taking time off and making less videos 
23:45 Josh gets shit carrying a wand around time making cross walk signs change 
24:20 Josh shows off his new snake skin staff 
25:50 Josh doesn't like taking a break from videos but he needed to 
26:10 Josh had some care packages and has already opened them, they contain food 
28:10 Josh talks about selling wands and trolls breaking them, that's bad juju on you 
29:00 Josh talks about spending holidays working on wands 
30:20 You'll get fucked with everything you do. Josh signs off like he usually would do'''

summary = summary.split('\n')

summary = [x for x in summary if x != '']

for x in summary:
    hms = []
    idx = x.find(timestampDelimiter)
    descr = x[idx+1:]
    ts = x[:idx]

    hmsEntry = ''
    for cnt, char in enumerate(ts):
        if char == ':':
            hms.append(hmsEntry)
            hmsEntry = ''
        else:
            hmsEntry = hmsEntry + char
            if cnt+1 == len(ts):
                hms.append(hmsEntry)
                hmsEntry = ''
    #    print(cnt, ts, char)
   # print(ts, descr, hmsEntry)
    
    if len(hms) == 2 :
        tsUrl = url + f'&t={hms[0]}m{hms[1]}s'

    if len(hms) == 3:
        tsUrl = url + f'&t={hms[0]}h{hms[1]}m{hms[2]}s'

    print(f'[{ts}]({tsUrl}) - {descr}\n')
