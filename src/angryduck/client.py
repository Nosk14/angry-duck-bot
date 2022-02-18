from discord import Client, RawReactionActionEvent, Message, RawMessageUpdateEvent, Object
from rules import VerifyUserRule, RemoveNonVerifiedMessagesWithLinksRule
import logging

VERIFICATION_MESSAGE_ID = 938516475113791558
VERIFICATION_CHANNEL_ID = 938352874168127529
VERIFIED_ROLE_ID = 938353848026812416
FRIEND_ROLE_ID = 938355921518735360
DUCK_EMOJI = "🦆"


class AngryDuckClient(Client):

    def __init__(self, logger: logging.Logger, **options):
        super().__init__(**options)
        self.logger = logger
        logging.getLogger('discord.gateway').setLevel(logging.WARNING)
        logging.getLogger('discord.client').setLevel(logging.WARNING)
        self.__set_up_rules()

    def __set_up_rules(self):
        self.verification_rule = VerifyUserRule(self.logger)
        self.remove_messages_with_links_rule = RemoveNonVerifiedMessagesWithLinksRule(self.logger)

    async def on_ready(self):
        self.logger.info("Angry Duck up and running!")

    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        await self.__apply_safely(self.remove_messages_with_links_rule, message.author, message)

    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        await self.__apply_safely(self.verification_rule, payload.message_id, payload.channel_id, payload.emoji.name, payload.member)

    async def on_error(self, event_method, *args, **kwargs):
        self.logger.error(f"Error during {event_method}: [{args}] [{kwargs}]")

    async def __apply_safely(self, rule, *args, **kargs):
        try:
            await rule.apply(*args, **kargs)
        except Exception as ex:
            self.logger.warning(f"Error applying rule: {rule.__class__.__name__} {ex}")




