from twitchio.ext import commands


OAUTH_PASSWORD, CLIENT_ID = open("secrets.txt", "r").read().split("\n")
NICKNAME = "RoboOritart"
CHANNEL = "Oritart"
ADMIN_COMMANDS = {}
COMMANDS = {}
f = open("data.txt", "r")
data = f.read().split("\n")
f.close()

decklist = data[0]
wins = int(data[1])
losses = int(data[2])
print(decklist)
print(wins)
print(losses)


bot = commands.Bot(
    irc_token=OAUTH_PASSWORD,
    client_id=CLIENT_ID,
    nick=NICKNAME,
    prefix="!",
    initial_channels=[CHANNEL]
)

def setup():
    ADMIN_COMMANDS["!decklist"] = save_decklist
    ADMIN_COMMANDS["!record"] = save_record
    ADMIN_COMMANDS["!stop"] = stop
    COMMANDS["!decklist"] = get_decklist
    COMMANDS["!record"] = get_record


@bot.event
async def event_ready():
    ws = bot._ws
    await ws.send_privmsg(CHANNEL, "Hello!")


@bot.event
async def event_message(context):
    author = context.author.name
    message = context.content
    if author.lower() == NICKNAME.lower():
        return
    if author.lower() == CHANNEL.lower():
        output = handle_admin_command(message)
    else:
        output = handle_command(message)
    if output and len(output) > 0:
        await context.channel.send(output)


def handle_admin_command(message):
    blah = message.split(" ")
    command = blah[0]
    if len(blah) == 1:
        return handle_command(message)
    arg = blah[1]
    func = ADMIN_COMMANDS.get(command, None)
    if func:
        return func(arg)


def handle_command(message):
    func = COMMANDS.get(message, None)
    if func:
        return func()
    print("not found")


def save_decklist(arg):
    global decklist
    decklist = arg
    save_data()
    return "Decklist saved"


def get_decklist():
    global decklist
    print(decklist)
    return "Decklist: " + decklist


def save_record(arg):
    global wins, losses
    if arg == "win":
        wins += 1
    if arg == "loss":
        losses += 1
    if arg == "clear":
        wins = 0
        losses = 0
    save_data()
    return "Record updated to " + str(wins) + "-" + str(losses)


def get_record():
    global wins, losses
    print(wins)
    print(losses)
    return "Currently " + str(wins) + "-" + str(losses)


def stop(arg):
    exit(0)


def save_data():
    global decklist, wins, losses
    d = decklist + "\n" + str(wins) + "\n" + str(losses)
    f = open("data.txt", "w")
    f.write(d)
    f.close()


if __name__ == "__main__":
    setup()
    bot.run()
