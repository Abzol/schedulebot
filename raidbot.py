#TODO COMMENT THIS SHIT
#TODO fnmatch (e.g. 'wed' matches 'wednesday')
import discord
import asyncio
import json

ADMIN = ["49627337024606208", #olivia
         ]
READY    = 2
NOTREADY = 1
NOTSURE  = 0

def makeday():
    with open('members', 'r') as f:
        members = json.loads(f.read())
        day = {}
        day['members'] = {}
        day['desc'] = ''
        for member in members:
            day['members'][member] = {'status' : NOTSURE, 'reason' : None}
    return day

def buildmessage(client, message, schedule):
    msg = ""
    try:
        for day in list(schedule.keys()):
            if (schedule[day]['description'] == ''):
                msg += ('\n**' + day + '**\n')
            else:
                msg += ('\n**' + day + '** *' +
                        schedule[day]['description'] + '* \n')
            for user in list(schedule[day]['members'].keys()):
                if (schedule[day]['members'][user]['status'] == NOTREADY):
                    msg += '<:negativebox:340066825922674688> '
                elif (schedule[day]['members'][user]['status'] == READY):
                    msg += ':white_check_mark: '
                else:
                    msg += '<:questionbox:340066786370256898> '
                name = ''
                for member in message.server.members:
                    if (member.id == user):
                        name = member.nick
                        if (name == None):
                            name = member.name
                        reason = schedule[day]['members'][member.id]['reason'] 
                        if not (reason == None or reason == ''):
                            name += ' *(%s)*' % (reason)
                        msg += name + '\n'
    except:
        msg = 'No raid days. Schedule some!'
        raise
    if (msg == ""):
        msg = 'Something happened.'
    return msg

@asyncio.coroutine
def updateMessage(client, message, schedule):
    msg = yield from client.get_message(message.channel,
                                        '343182358247243777') 
    yield from client.edit_message(msg, buildmessage(client,
                                                     message,
                                                     schedule))
    return

@asyncio.coroutine
def raid(client, message):
    with open('raids', 'r') as f:
        query = " ".join(message.content.split()[1:]).lower()
        command = query.split()[0]
        day = query.split()[1]
        try:
            desc = " ".join(query.split()[2:])
        except IndexError:
            desc = ''
        schedule = json.loads(f.read())
        if (command.startswith('add') or command.startswith('clear')):
            schedule[day] = makeday()
            schedule[day]['description'] = desc
        if (command.startswith('remove')):
            del schedule[day]
    with open('raids', 'w') as f:
        f.write(json.dumps(schedule))
    yield from updateMessage(client, message, schedule)

@asyncio.coroutine
def setup(client, message):
    try:
        if (message.author.id in ADMIN):
            users = message.mentions        
            members = []
            for user in users:
                members.append(user.id)
            with open('members', 'w') as f:
                f.write(json.dumps(members))
        yield from client.send_message(message.channel,
                                       buildmessage(client, message, {}))
    except:
        pass

@asyncio.coroutine
def lookup(client, message, fname):
    yield from client.send_message(message.channel, msg)

@asyncio.coroutine
def dryrun(client, message):
    with open('raids', 'r') as f:
        schedule = json.loads(f.read())
        yield from client.send_message(message.channel,
                                       buildmessage(schedule))
@asyncio.coroutine
def digest(client, message):
    author = message.author.id
    operator = message.content[0]
    day = message.content.split()[0][1:]
    reason = " ".join(message.content.split()[1:])
    schedule = {}
    try:
        with open('raids', 'r') as f:
            schedule = json.loads(f.read())
        if (operator == '+'):
            schedule[day]['members'][author]['status'] = READY
            schedule[day]['members'][author]['reason'] = reason
        elif (operator == '-'):
            schedule[day]['members'][author]['status'] = NOTREADY
            schedule[day]['members'][author]['reason'] = reason
        elif (operator == '?'):
            schedule[day]['members'][author]['status'] = NOTSURE
            schedule[day]['members'][author]['reason'] = reason
        else:
            return
        with open('raids', 'w') as f:
            f.write(json.dumps(schedule))
        yield from updateMessage(client, message, schedule)
    except KeyError:
        return 0

def parse(client, message):
    if (message.channel.name == 'raid-calendar'):
        if (message.content.lower().startswith('!raid')):
            yield from raid(client, message)
        elif (message.content.lower().startswith('!setup')):
            yield from setup(client, message)
        elif (message.content.lower().startswith('!dry-run')):
            yield from dryrun(client, message)
        else:
            yield from digest(client, message)
        yield from client.delete_message(message)

if __name__ == "__main__":
    print("This is a modular bot file. Please invoke it from a base bot.")
