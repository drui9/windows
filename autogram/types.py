from enum import StrEnum, Enum, auto


# --<> Update Enum
class UpdateType(StrEnum):
    message = "message"
    message_edit = "edited_message"
    channel_post = "channel_post"
    channel_post_edit = "edited_channel_post"
    business_connection = "business_connection"
    business_message = "business_message"
    business_message_edit = "edited_business_message"
    business_message_delete = "deleted_business_message"
    message_reaction = "message_reaction"
    message_reaction_count = "message_reaction_count"
    inline = "inline_query"
    chosen_inline_result = "chosen_inline_result"
    callback = "callback_query"
    shipping = "shipping_query"
    pre_checkout = "pre_checkout_query"
    purchased_paid_media = "purchased_paid_media"
    poll = "poll"
    poll_answer = "poll_answer"
    my_chat_member = "my_chat_member"
    chat_member = "chat_member"
    chat_join_request = "chat_join_request"
    chat_boost = "chat_boost"
    chat_boost_removed = "removed_chat_boost"

    # --</>


# --<>
class EventType(Enum):
    private_chat_message = auto()
    private_chat_ban = auto()
    private_chat_unban = auto()
    private_chat_image = auto()
    private_chat_audio = auto()
    private_chat_video = auto()
    private_chat_document = auto()
    private_chat_location = auto()
    private_chat_reaction = auto()
    private_chat_entity = auto()
    group_message = auto()
    group_member_joined = auto()
    group_member_left = auto()
    channel_message = auto()
    channel_member_joined = auto()
    channel_member_left = auto()
    supergroup_message = auto()
    supergroup_member_joined = auto()
    supergroup_member_left = auto()
    chat_upgrade = auto()
