from discord import Object, Member
import logging


class VerifyUserRule:
    VERIFICATION_MESSAGE_ID = 938516475113791558
    VERIFICATION_CHANNEL_ID = 938352874168127529
    VERIFIED_ROLE_ID = 938353848026812416
    DUCK_EMOJI = "🦆"

    def apply(self, message_id, channel_id, emoji_name, member: Member):
        if message_id == VerifyUserRule.VERIFICATION_MESSAGE_ID \
                and channel_id == VerifyUserRule.VERIFICATION_CHANNEL_ID \
                and emoji_name == VerifyUserRule.DUCK_EMOJI:
            await member.add_roles(Object(id=VerifyUserRule.VERIFIED_ROLE_ID), reason="Automatic ducky verification.")
            logging.info(f"User {member.display_name} has been verified.")


class RemoveNonVerifiedMessagesWithLinksRule:

    def apply(self):
        pass

    def __contents_any_link(self, message):
        pass

    def __is_verified_user(self, user):
        pass


class RemoveSuspiciousMessagesRule:

    def __init__(self):
        pass

    def apply(self):
        pass

