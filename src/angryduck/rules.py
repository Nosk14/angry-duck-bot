from discord import Object, Member, Message
import discord
import logging


class VerifyUserRule:
    VERIFICATION_MESSAGE_ID = 938516475113791558
    VERIFICATION_CHANNEL_ID = 938352874168127529
    VERIFIED_ROLE_ID = 938353848026812416
    DUCK_EMOJI = "🦆"

    def __init__(self, logger):
        self.logger = logger

    async def apply(self, message_id, channel_id, emoji_name, member: Member):
        if message_id == VerifyUserRule.VERIFICATION_MESSAGE_ID \
                and channel_id == VerifyUserRule.VERIFICATION_CHANNEL_ID \
                and emoji_name == VerifyUserRule.DUCK_EMOJI:
            await member.add_roles(Object(id=VerifyUserRule.VERIFIED_ROLE_ID), reason="Automatic ducky verification.")
            self.logger.info(f"[{self.__class__.__name__}] User {member} has been verified.")


class RemoveNonVerifiedMessagesWithLinksRule:

    def __init__(self, logger):
        self.logger = logger

    async def apply(self, member: Member, message: Message):
        if not self.__has_verified_role(member) and self.__contents_any_link(message):
            try:
                await message.delete()
                logging.info(f"[{self.__class__.__name__}] Deleted message from {message.author}")
            except discord.NotFound:
                self.logger.warning(f"[{self.__class__.__name__}] Message not found trying to remove it.")

    def __contents_any_link(self, message: Message):
        return 'http://' in message.content or 'https://' in message.content

    def __has_verified_role(self, member):
        return next(filter(lambda r: r.id == VerifyUserRule.VERIFIED_ROLE_ID, member.roles), False)


class RemoveSuspiciousMessagesRule:

    def __init__(self):
        pass

    async def apply(self, member: Member, message: Message):
        pass

