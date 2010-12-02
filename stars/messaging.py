class Publisher:
    """ """
    def __init__(self,broker=None):
        self.add_broker(broker)
    
    def publish(self,message):
        if self.broker:
            self.broker.process(sender=self,payload=message)

    def add_broker(self,broker):
        self.broker=broker
        broker.add_publisher(self)

    def remove_broker(self):
        if self.broker:
            self.broker.remove_publisher(self)
            self.broker=None

    
class Subscriber:
    """ """
    def __init__(self,broker):
        self.brokers={}
        self.subscribe(broker)

    def subscribe(self,broker):
        broker.add_subscriber(self)
        self.brokers[broker]=broker

    def receive(self,message):
        print 'in subscriber: ',self,message

    def unsubscribe(self,broker):
        if broker in self.brokers:
            self.brokers.pop(broker)
            self.brokers[broker]

class Broker:
    """ """
    def __init__(self):
        self.publishers={}
        self.subscribers={}

    def add_publisher(self,publisher):
        self.publishers[publisher]=publisher

    def remove_publisher(self,publisher):
        if publisher in self.publishers:
            self.publishers.pop(publisher)

    def add_subscriber(self,subscriber):
        self.subscribers[subscriber]=subscriber

    def remove_subscriber(self,subscriber):
        if subscriber in self.subscribers:
            self.subscribers.pop(subscriber)

    def process(self,sender=None,payload=None):
        print 'in broker: ',payload
        self.remove_subscriber(sender)
        for subscriber in self.subscribers:
            self.subscribers[subscriber].receive(payload)
        self.add_subscriber(sender)

class PubSub(Publisher,Subscriber):
    def __init__(self,broker):
        Publisher.__init__(self,broker)
        Subscriber.__init__(self,broker)

class Interactions:
    """Manager of Interactions"""
    def __init__(self):
        self.interactions={}
        self.origin_types={}
        self.destination_types={}
        self.modes={}
        self.origin_modes={}

    def add_interaction(self,interaction):
        self.interactions[interaction.key]=interaction
        if interaction.origin_type not in self.origin_types:
            self.origin_types[interaction.origin_type]=[]
        self.origin_types[interaction.origin_type].append(interaction.key)
        if interaction.mode not in self.modes:
            self.modes[interaction.mode]=[]
        self.modes[interaction.mode].append(interaction.key)

        om_key=interaction.origin_type+"_"+interaction.mode
        if om_key not in self.origin_modes:
            self.origin_modes[om_key]=[]
        self.origin_modes[om_key].append(interaction.key)

class Interaction:
    """
    Interaction between an origin View type and destination View type
    
    Parameters
    ==========

    origin_type: string
                 origin view type
    
    destination_type: string
                 destination view type

    origin_event: string
                 name of event on origin view

    destination_event: string
                 name of event to be called on destination view

    mode: string
          interaction mode in effect at time origin event was fired
    
    """
    def __init__(self,origin_type,destination_type,
            origin_event,destination_event,mode,manager=None):
        self.origin_type=origin_type
        self.destination_type=destination_type
        self.origin_event=origin_event
        self.destination_event=destination_event
        self.mode=mode
        self.key=",".join((origin_type,destination_type,origin_event,
                destination_event,mode))
        if manager:
            manager.add_interaction(self)
            self.manager=manager

if __name__ == '__main__':

    # example of how this all can be used

    broker=Broker()
    class View(PubSub):
        """ """
        def __init__(self,name,type,broker):
            self.name=name
            self.type=type
            self.broker=broker
            PubSub.__init__(self,broker)

        def __repr__(self):
            return "View type: %s, name: %s"%(self.type,self.name)

    # interactions
    interactions=Interactions()
    view_types='scatter','map','density','table'
    modes='linking','brushing','extended_linking','extended_brushing'
    for mode in modes:
        for origin in view_types:
            for destination in view_types:
                Interaction(origin,destination,'select_observations','select_observations',
                        mode,interactions)

    views=[]
    for view_type in view_types:
        views.extend([View("%s_%d"%(view_type[0],i),view_type,broker) for i in range(5)])
