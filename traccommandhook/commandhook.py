from subprocess import call

from trac.core import Component, implements
from trac.ticket.api import ITicketChangeListener

from unidecode import unidecode


def shouldNotify(ticket, old_values, handledPriorities):
    if 'status' in old_values and old_values['status'] == u'closed':
        # ticket status was closed
        if ticket['status'] == u'reopened' and \
           ticket['priority'] in handledPriorities:
            # ticket was reopened and should be notified
            return True
    elif not 'priority' in old_values:
        # ticket priority didn't change, no need to notify (was already done
        # if needed)
        return False
    elif ticket['priority'] in handledPriorities and \
            ticket['status'] != u'closed':
        # we should notify only if ticket is not closed
        return True
    return False


def createCommandStringWithParams(configOptions, ticket, command):
    """
    Constructs a list with the command and its parameters
    """
    optionList = configOptions('commandhook')
    parameters = {}
    for name, value in optionList:
        if 'param' not in name:
            continue

        if name.endswith('-fields'):
            paramName = name.split('-fields')[0]
            values = []

            for v in value.split(','):
                if v.startswith('"') and v.endswith('"'):
                    val = v[1:-1]
                else:
                    val = ticket.get_value_or_default(v) or getattr(ticket, v, '',)
                if isinstance(val, int):
                    val = unicode(str(val))
                if not isinstance(val, unicode):
                    val = unicode(val)
                values.append(unidecode(val))

            if paramName in parameters:
                parameters[paramName]['content'] = ''.join(values).strip()
            else:
                parameters[paramName] = {'content': ''.join(values).strip()}

        elif name.endswith('-parameter'):
            paramName = name.split('-parameter')[0]
            if paramName in parameters:
                parameters[paramName]['param'] = value
            else:
                parameters[paramName] = {'param': value}

    commandWithParams = [command]
    for title, param in parameters.items():
        commandWithParams.append(param['param'])
        commandWithParams.append(param['content'])
    return commandWithParams


class TracCommandHook(Component):
    implements(ITicketChangeListener)

    def ticket_created(self, ticket):
        """
        Called when a ticket is created.
        """
        env = self.env
        handledPriorities = env.config.getlist('commandhook', 'priorities')
        if ticket['priority'] not in handledPriorities:
            return
        command = env.config.get('commandhook', 'command')
        commandWithParams = createCommandStringWithParams(env.config.options,
                                                          ticket,
                                                          command)
        call(commandWithParams)
        env.log.debug("Ticket %s created. Command executed !" % ticket.id)

    def ticket_changed(self, ticket, comment, author, old_values):
        """
        Called when a ticket is modified.
        """
        env = self.env
        handledPriorities = env.config.getlist('commandhook', 'priorities')
        if not shouldNotify(ticket, old_values, handledPriorities):
            return
        command = env.config.get('commandhook', 'command')
        commandWithParams = createCommandStringWithParams(env.config.options,
                                                          ticket,
                                                          command)
        call(commandWithParams)
        env.log.debug("Ticket %s changed. Command executed !" % ticket.id)

    def ticket_deleted(self, ticket):
        """
        Called when a ticket is deleted.
        Nothing to do here ...
        """
