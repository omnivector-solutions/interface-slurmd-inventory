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

        # Set the node inventory data on the relation on_relation_created
        event.relation.data[self.model.unit]['inventory'] = json.dumps({
            'NodeName': self.hostname,
            'CPUs': '4',
            'Boards': '1',
            'SocketsPerBoard': '1',
            'CoresPerSocket': '4',
            'ThreadsPerCore': '1',
            'RealMemory': '7852',
            'UpTime': '0-08:49:20',
        })

    def _on_relation_joined(self, event):
        logger.debug("###### LOGGING RELATION JOINED ######")

    def _on_relation_changed(self, event):
        logger.debug("###### LOGGING RELATION CHANGED ######")

        nodes_info = [event.relation.data[self.model.unit]['inventory']]
        for unit in event.relation.units:
            inventory = event.relation.data[unit]['inventory']
            nodes_info.append(inventory)
        self._state.nodes_info = nodes_info

        self.on.slurmd_inventory_available.emit()

    def _on_relation_departed(self, event):
        logger.debug("###### LOGGING RELATION DEPARTED ######")

    def _on_relation_broken(self, event):
        logger.debug("###### LOGGING RELATION BROKEN ######")
