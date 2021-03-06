import kirc
import sys
import select
import commands

irc = kirc.Irc('Rusnet', 'irc.run.net', 6660,
               'Coxy_t', 'bot', 'kupp bot', 'utf-8')
irc.connect(100, 900)
irc.join('#16bits')
irc.join('###kupp_tests')
c = commands.CommandsCore(irc, '.')
ready = select.select([sys.stdin], [], [], 0.1)[0]
while True:
    try:
        msgs = irc.wait_data()
        if msgs:
            for msg in msgs.split('\r\n'):
                if msg:
                    irc.maintenance(msg)
                    kirc.pretty_print(msg.strip())
                    c.search(msg)
    except KeyboardInterrupt:
        irc.quit('Im part, but it doesnt mean that i crash')
    except kirc.IrcConnectionError:
        irc.reconnect(100, 900)
