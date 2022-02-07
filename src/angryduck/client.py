from discord import Client, RawReactionActionEvent, RawMessageUpdateEvent, Object
from logging import Logger

VERIFICATION_MESSAGE_ID = 938516475113791558
VERIFICATION_CHANNEL_ID = 938352874168127529
VERIFIED_ROLE_ID = 938353848026812416
FRIEND_ROLE_ID = 938355921518735360
DUCK_EMOJI = "🦆"


class AngryDuckClient(Client):

    def __init__(self, logger: Logger, **options):
        super().__init__(**options)
        self.logger = logger

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
        if payload.message_id == VERIFICATION_MESSAGE_ID and payload.channel_id == VERIFICATION_CHANNEL_ID and payload.emoji.name == DUCK_EMOJI:
            await payload.member.add_roles(Object(id=VERIFIED_ROLE_ID), reason="Automatic ducky verification.")

    async def on_error(self, event_method, *args, **kwargs):
        self.logger.error(f"Error during {event_method}: [{args}] [{kwargs}]")

    # def __delete_message_with_links(self, message):
    #     content = message.content.lower()
    #     if 'https://' in content or 'http://' in content:
    #         message.delete()




