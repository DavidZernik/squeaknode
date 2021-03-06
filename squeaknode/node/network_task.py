import logging
import threading

from squeaknode.network.peer_client import PeerClient
from squeaknode.node.peer_task import PeerSyncTask

logger = logging.getLogger(__name__)


LOOKUP_BLOCK_INTERVAL = 1008  # 1 week


class NetworkSyncTask:
    def __init__(
        self,
        squeak_store,
        postgres_db,
        lightning_client,
    ):
        self.squeak_store = squeak_store
        self.postgres_db = postgres_db
        self.lightning_client = lightning_client

    def sync(self, peers):
        logger.debug("Network sync for class {}".format(
            self.__class__,
        ))
        for peer in peers:
            sync_peer_thread = threading.Thread(
                target=self.sync_peer,
                args=(peer,),
            )
            sync_peer_thread.start()

    def sync_peer(self, peer):
        # peer_upload = PeerUpload(
        #     peer,
        #     self.squeak_store,
        #     self.postgres_db,
        #     self.lightning_client,
        # )
        # try:
        #     logger.debug("Trying to upload to peer: {}".format(peer))
        #     with self.UploadingContextManager(
        #         peer, peer_upload, self.squeak_sync_status
        #     ) as uploading_manager:
        #         peer_upload.upload(block_height)
        # except Exception as e:
        #     logger.error("Upload from peer failed.", exc_info=True)
        pass


class DownloadTimelineNetworkSyncTask(NetworkSyncTask):
    def __init__(
        self,
        squeak_store,
        postgres_db,
        lightning_client,
        block_height,
    ):
        super().__init__(squeak_store, postgres_db, lightning_client)
        self.block_height = block_height

    def sync_peer(self, peer):
        if not peer.downloading:
            return
        peer_sync_task = PeerSyncTask(
            peer,
            self.squeak_store,
            self.postgres_db,
            self.lightning_client,
        )
        try:
            logger.debug("Trying to download with block height: {}".format(self.block_height))
            peer_sync_task.download(self.block_height)
        except Exception as e:
            logger.error("Download from peer failed.", exc_info=True)

class UploadTimelineNetworkSyncTask(NetworkSyncTask):
    def __init__(
        self,
        squeak_store,
        postgres_db,
        lightning_client,
        block_height,
    ):
        super().__init__(squeak_store, postgres_db, lightning_client)
        self.block_height = block_height

    def sync_peer(self, peer):
        if not peer.uploading:
            return
        peer_sync_task = PeerSyncTask(
            peer,
            self.squeak_store,
            self.postgres_db,
            self.lightning_client,
        )
        try:
            logger.debug("Trying to upload with block height: {}".format(self.block_height))
            peer_sync_task.upload(self.block_height)
        except Exception as e:
            logger.error("Upload from peer failed.", exc_info=True)

class SingleSqueakNetworkSyncTask(NetworkSyncTask):
    def __init__(
        self,
        squeak_store,
        postgres_db,
        lightning_client,
        squeak_hash,
    ):
        super().__init__(squeak_store, postgres_db, lightning_client)
        self.squeak_hash = squeak_hash

    def sync_peer(self, peer):
        if not peer.downloading:
            return
        peer_sync_task = PeerSyncTask(
            peer,
            self.squeak_store,
            self.postgres_db,
            self.lightning_client,
        )
        try:
            logger.debug("Trying to download single squeak {}".format(self.squeak_hash))
            peer_sync_task.download_single_squeak(self.squeak_hash)
        except Exception as e:
            logger.error("Download single squeak from peer failed.", exc_info=True)
