import logging
import socket
import json

from ops.framework import (
    EventBase,
    EventSource,
    Object,
    ObjectEvents,
    StoredState,
)


logger = logging.getLogger()


class SlurmdInventoryAvailableEvent(EventBase):
    """Slurmd Peer Available Event"""


class SlurmdPeerRelationEvents(ObjectEvents):
    """Peer Relation Events"""
    slurmd_inventory_available = EventSource(SlurmdInventoryAvailableEvent)


class SlurmdPeer(Object):

    _state = StoredState()
    on = SlurmdPeerRelationEvents()

    def __init__(self, charm, relation_name):
        super().__init__(charm, relation_name)

        self._state.set_default(nodes_info=list())

        self.hostname = socket.gethostname()

        self.framework.observe(
            charm.on[relation_name].relation_created,
            self._on_relation_created
        )

        self.framework.observe(
            charm.on[relation_name].relation_joined,
            self._on_relation_joined
        )

        self.framework.observe(
            charm.on[relation_name].relation_changed,
            self._on_relation_changed
        )

        self.framework.observe(
            charm.on[relation_name].relation_departed,
            self._on_relation_departed
        )

        self.framework.observe(
            charm.on[relation_name].relation_broken,
            self._on_relation_broken
        )

    def get_slurmd_inventory(self):
        """Return the inventory of all slurmd nodes.
        """
        return [node_inventory for node_inventory in self._state.nodes_info]

    def _on_relation_created(self, event):
        logger.debug("###### LOGGING RELATION CREATED ######")

        node_info = json.dumps({
            'inventory': {
                'NodeName': self.hostname,
                'CPUs': '4',
                'Boards': '1',
                'SocketsPerBoard': '1',
                'CoresPerSocket': '4',
                'ThreadsPerCore': '1',
                'RealMemory': '7852',
                'UpTime': '0-08:49:20',
            },
            'hostname': self.hostname,
            'ingress_address': "127.6.6.6",
            'partition': "debug",
        })
        logger.debug(node_info)
        # Set the node_info to the unit data for the peer relation
        event.relation.data[self.model.unit]['node_info'] = node_info
        # Add this units data to the local state
        self._state.nodes_info.append(node_info)
        # Emit the slurmd_inventory_available event
        self.on.slurmd_inventory_available.emit()

    def _on_relation_joined(self, event):
        logger.debug("###### LOGGING RELATION JOINED ######")

    def _on_relation_changed(self, event):
        logger.debug("###### LOGGING RELATION CHANGED ######")

        for unit in event.relation.units:
            node_info = json.loads(event.relation.data[unit]['node_info'])
            self._nodes_info.append(node_info)

        logger.debug([node for node in self._nodes_info])

        self.on.slurmd_inventory_available.emit()

    def _on_relation_departed(self, event):
        logger.debug("###### LOGGING RELATION DEPARTED ######")

    def _on_relation_broken(self, event):
        logger.debug("###### LOGGING RELATION BROKEN ######")
