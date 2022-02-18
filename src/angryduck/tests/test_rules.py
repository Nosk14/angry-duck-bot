from unittest import TestCase, IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch
from rules import VerifyUserRule, RemoveNonVerifiedMessagesWithLinksRule
import discord
import logging
import aiohttp


class TestVerifyUserRule(IsolatedAsyncioTestCase):
    VERIFICATION_MESSAGE_ID = 938516475113791558
    VERIFICATION_CHANNEL_ID = 938352874168127529
    VERIFIED_ROLE_ID = 938353848026812416
    DUCK_EMOJI = "🦆"

    def setUp(self):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        self.rule = VerifyUserRule(logger)

    @patch('discord.Member')
    async def test_apply_role(self, member):
        member.add_roles = AsyncMock(return_value=None)

        await self.rule.apply(
            TestVerifyUserRule.VERIFICATION_MESSAGE_ID,
            TestVerifyUserRule.VERIFICATION_CHANNEL_ID,
            TestVerifyUserRule.DUCK_EMOJI,
            member)

        member.add_roles.assert_called_once()
        applied_role_id = member.add_roles.call_args[0][0].id
        self.assertEqual(TestVerifyUserRule.VERIFIED_ROLE_ID, applied_role_id)

    @patch('discord.Member')
    async def test_do_not_apply_role_wrong_emoji(self, member):
        member.add_roles = AsyncMock(return_value=None)

        await self.rule.apply(
            TestVerifyUserRule.VERIFICATION_MESSAGE_ID,
            TestVerifyUserRule.VERIFICATION_CHANNEL_ID,
            "😄",
            member)

        member.add_roles.assert_not_called()

    @patch('discord.Member')
    async def test_do_not_apply_role_wrong_channel(self, member):
        member.add_roles = AsyncMock(return_value=None)

        await self.rule.apply(
            TestVerifyUserRule.VERIFICATION_MESSAGE_ID,
            0,
            TestVerifyUserRule.DUCK_EMOJI,
            member)

        member.add_roles.assert_not_called()

    @patch('discord.Member')
    async def test_do_not_apply_role_wrong_message(self, member):
        member.add_roles = AsyncMock(return_value=None)

        await self.rule.apply(
            0,
            TestVerifyUserRule.VERIFICATION_CHANNEL_ID,
            TestVerifyUserRule.DUCK_EMOJI,
            member)

        member.add_roles.assert_not_called()


class TestRemoveNonVerifiedMessagesWithLinksRule(IsolatedAsyncioTestCase):
    VERIFIED_ROLE_ID = 938353848026812416

    def setUp(self):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        self.rule = RemoveNonVerifiedMessagesWithLinksRule(logger)

    @patch('discord.Member')
    @patch('discord.Message')
    async def test_remove_message(self, member, message):
        message.delete = AsyncMock()
        member.roles = [discord.Object(id=0)]
        message.content = "This message has a link https://google.es"

        await self.rule.apply(member, message)

        message.delete.assert_called_once()

    @patch('discord.Member')
    @patch('discord.Message')
    @patch('aiohttp.ClientResponse')
    async def test_remove_already_removed_message(self, member, message, response):
        def raise_not_found():
            response.status = 404
            raise discord.NotFound(response, message)
        message.delete = AsyncMock(side_effect=raise_not_found)
        message.content = "This message has a link https://google.es"
        member.roles = [discord.Object(id=0)]

        await self.rule.apply(member, message)

        message.delete.assert_called_once()

    @patch('discord.Member')
    @patch('discord.Message')
    async def test_do_not_remove_message_when_verified(self, member, message):
        message.delete = AsyncMock()
        member.roles = [discord.Object(id=0), discord.Object(id=TestRemoveNonVerifiedMessagesWithLinksRule.VERIFIED_ROLE_ID)]
        message.content = "This message has a link https://google.es"

        await self.rule.apply(member, message)

        message.delete.assert_not_called()

    @patch('discord.Member')
    @patch('discord.Message')
    async def test_do_not_remove_message_when_no_links(self, member, message):
        message.delete = AsyncMock()
        member.roles = [discord.Object(id=0)]
        message.content = "This message has no link"

        await self.rule.apply(member, message)

        message.delete.assert_not_called()
