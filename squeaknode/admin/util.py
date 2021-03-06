from squeaknode.server.util import get_hash, get_replyto

from proto import squeak_admin_pb2, squeak_admin_pb2_grpc


def squeak_entry_to_message(squeak_entry_with_profile):
    if squeak_entry_with_profile is None:
        return None
    squeak_entry = squeak_entry_with_profile.squeak_entry
    squeak = squeak_entry.squeak
    block_header = squeak_entry.block_header
    is_unlocked = squeak.HasDecryptionKey()
    content_str = squeak.GetDecryptedContentStr() if is_unlocked else None
    squeak_profile = squeak_entry_with_profile.squeak_profile
    is_author_known = squeak_profile is not None
    author_name = squeak_profile.profile_name if squeak_profile else None
    author_address = str(squeak.GetAddress())
    is_reply = squeak.is_reply
    reply_to = get_replyto(squeak).hex() if is_reply else None
    return squeak_admin_pb2.SqueakDisplayEntry(
        squeak_hash=get_hash(squeak).hex(),
        is_unlocked=squeak.HasDecryptionKey(),
        content_str=content_str,
        block_height=squeak.nBlockHeight,
        block_hash=squeak.hashBlock.hex(),
        block_time=block_header.nTime,
        is_author_known=is_author_known,
        author_name=author_name,
        author_address=author_address,
        is_reply=is_reply,
        reply_to=reply_to,
    )

def squeak_profile_to_message(squeak_profile):
    if squeak_profile is None:
        return None
    has_private_key = squeak_profile.private_key is not None
    return squeak_admin_pb2.SqueakProfile(
        profile_id=squeak_profile.profile_id,
        profile_name=squeak_profile.profile_name,
        has_private_key=has_private_key,
        address=squeak_profile.address,
        sharing=squeak_profile.sharing,
        following=squeak_profile.following,
        whitelisted=squeak_profile.whitelisted,
    )

def squeak_peer_to_message(squeak_peer):
    if squeak_peer is None:
        return None
    return squeak_admin_pb2.SqueakPeer(
        peer_id=squeak_peer.peer_id,
        peer_name=squeak_peer.peer_name,
        host=squeak_peer.host,
        port=squeak_peer.port,
        uploading=squeak_peer.uploading,
        downloading=squeak_peer.downloading,
    )

def offer_entry_to_message(offer_entry):
    if offer_entry is None:
        return None
    offer = offer_entry.offer
    peer = squeak_peer_to_message(offer_entry.peer)
    return squeak_admin_pb2.OfferDisplayEntry(
        offer_id=offer.offer_id,
        squeak_hash=offer.squeak_hash,
        amount=offer.price_msat,
        node_pubkey=offer.destination,
        node_host=offer.node_host,
        node_port=offer.node_port,
        peer=peer,
        invoice_timestamp=offer.invoice_timestamp,
        invoice_expiry=offer.invoice_expiry,
    )

def sent_payment_to_message(sent_payment):
    if sent_payment is None:
        return None
    return squeak_admin_pb2.SentPayment(
        sent_payment_id=sent_payment.sent_payment_id,
        offer_id=sent_payment.offer_id,
        peer_id=sent_payment.peer_id,
        squeak_hash=sent_payment.squeak_hash,
        preimage_hash=sent_payment.preimage_hash,
        preimage=sent_payment.preimage,
        amount=sent_payment.amount,
        node_pubkey=sent_payment.node_pubkey,
        preimage_is_valid=sent_payment.preimage_is_valid,
    )
