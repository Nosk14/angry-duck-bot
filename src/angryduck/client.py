from discord import Client, RawReactionActionEvent, RawMessageUpdateEvent, Object
from rules import VerifyUserRule
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
        self.verification_rule = VerifyUserRule()

    async def on_ready(self):
        self.logger.info("Angry Duck up and running!")

    # async def on_message(self, message):
    #     if message.author == self.user:
    #         return
    #     self.__delete_message_with_links(message)
    #
    # async def on_raw_message_edit(self, payload: RawMessageUpdateEvent):
    #     message = await self.get_channel(payload.channel_id).fetch_message(payload.message_id)
    #     self.__delete_message_with_links(message)

    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        self.verification_rule.apply(payload.message_id, payload.channel_id, payload.emoji.name, payload.member)

    async def on_error(self, event_method, *args, **kwargs):
        self.logger.error(f"Error during {event_method}: [{args}] [{kwargs}]")

    # def __delete_message_with_links(self, message):
    #     content = message.content.lower()
    #     if 'https://' in content or 'http://' in content:
    #         message.delete()




